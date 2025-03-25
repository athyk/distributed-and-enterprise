import traceback
from datetime import datetime, UTC, timedelta
from math import inf

import grpc
from werkzeug.security import check_password_hash, generate_password_hash

from backend.accounts.verification.email_verification import verify_email, send_verification_code_email
from backend.accounts.database.database import get_db
from backend.accounts.database.models import User, UserTag
from backend.common.proto import accounts_pb2_grpc, accounts_pb2, degree_pb2, tag_pb2
from backend.common.services import TagsClient, DegreesClient, AccountsClient
from backend.common.utils import verify_string, verify_integer, verify_list


class AccountsServicer(accounts_pb2_grpc.AccountsServicer):
    def Register(self, req: accounts_pb2.RegistrationRequest,
                 context: grpc.ServicerContext) -> accounts_pb2.LoginResponse:
        """
        Register allows the registration of a user.

        If OTP is not sent, the user will be emailed with the code.
        If a valid OTP is sent, the user will be logged in, ensure other fields are correct.
        """
        email_verify, email_error = verify_string(req.email, 4, 255, 'Email')  # Cannot exceed 255 rfc3696
        password_verify, password_error = verify_string(req.password, 8, inf, 'Password')
        first_name_verify, first_name_error = verify_string(req.first_name, 1, inf, 'First Name')
        last_name_verify, last_name_error = verify_string(req.last_name, 1, inf, 'Last Name')
        gender_verify, gender_error = verify_string(req.gender, 4, 12, 'Gender')
        degree_id_verify, degree_id_error = verify_integer(req.degree_id, 1, inf, 'Degree ID')
        year_of_study_verify, year_of_study_error = verify_integer(req.year_of_study, 1, 9, 'Year Of Study')
        tag_verify, tag_error = verify_list(list(req.tags), 0, 5, 'Tags')
        req.rank = req.rank.lower()

        # dates are validated below

        if False in [email_verify, password_verify, first_name_verify, last_name_verify,
                     gender_verify, degree_id_verify, year_of_study_verify, tag_verify]:
            all_errors = [email_error, password_error, first_name_error, last_name_error,
                          gender_error, degree_id_error, year_of_study_error, tag_error]

            error_messages = [item for item in all_errors if item.strip()]

            return accounts_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=error_messages,
            )

        try:
            dob = datetime.strptime(req.date_of_birth, "%d-%m-%Y").date()
            grad_date = datetime.strptime(req.grad_date, "%d-%m-%Y").date()
        except Exception:
            return accounts_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=['Dates Not Formatted Correctly'],
            )

        try:
            with get_db() as session:
                user = session.query(User).filter(User.email == req.email).first()

            if user:
                return accounts_pb2.LoginResponse(
                    success=False,
                    http_status=400,
                    error_message=['Email Already In Use'],
                )

            degree_client = DegreesClient()
            degree = degree_client.get(degree_pb2.DegreeGetRequest(id=req.degree_id))
            if not degree.success:
                return accounts_pb2.LoginResponse(
                    success=False,
                    http_status=400,
                    error_message=['Degree Not Found'],
                )

            # Could always store degree name for response

            user = User(
                email=req.email,
                password=generate_password_hash(req.password),
                first_name=req.first_name,
                last_name=req.last_name,
                email_verified=False,
                date_of_birth=dob,
                gender=req.gender,
                degree_id=req.degree_id,
                year_of_study=req.year_of_study,
                grad_date=grad_date,
                # TODO: placeholder profile_url
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            tag_client = TagsClient()

            for tag in req.tags:
                res = tag_client.create(tag_pb2.TagCreateRequest(id=tag))

                if res.success:  # Never assume the tag was created, do not error out either
                    user_tag = UserTag(user_id=user.id, tag_id=tag)
                    session.add(user_tag)

            session.commit()
        except Exception:
            traceback.print_exc()
            return accounts_pb2.LoginResponse(
                success=False,
                http_status=500,
                error_message=['An Unknown Error Occurred'],
            )

        if req.skip_email:
            return accounts_pb2.LoginResponse(
                success=True,
                http_status=201,
                user_id=user.id,
                otp_required=False,
            )

        success, message, otp_seed = send_verification_code_email(req.email)

        if success:
            account_client = AccountsClient()
            account_client.save_otp(user.id, str(otp_seed))
            return accounts_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user.id,
                otp_required=True,
            )

        return accounts_pb2.LoginResponse(
            success=False,
            http_status=500,
            error_message=['Error Sending Out Verification Email', message],
        )

    def Login(self, req: accounts_pb2.LoginRequest, context: grpc.ServicerContext) -> accounts_pb2.LoginResponse:
        """
        Login allows the login of a user,

        If OTP is not sent, the user will be emailed with the code.
        If a valid OTP is sent, the user will be logged in, ensure other fields are correct.
        """
        email_verify, email_error = verify_string(req.email, 4, 255, 'Email')  # Cannot exceed 255 rfc3696
        password_verify, password_error = verify_string(req.password, 8, inf, 'Password')

        if False in [email_verify, password_verify]:
            all_errors = [email_error, password_error]
            error_messages = [item for item in all_errors if item.strip()]

            return accounts_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=error_messages,
            )

        with get_db() as session:
            # TODO: use AccountsClient to fetch from cache
            user: User | None = session.query(User).filter(User.email == req.email).first()

        # Handle both user not found and invalid password as the same response as they should produce
        # the same error.
        if user is None or not check_password_hash(user.password, req.password):
            return accounts_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=["Invalid email or password."],
            )

        if user.email_verified or req.skip_email:
            return accounts_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user.id,
                user=user.to_dict(),
                otp_required=False,
            )

        accounts_client = AccountsClient()
        email_verify_id = accounts_client.get_otp(user.id)

        if not email_verify_id:  # If no otp is in cache.
            return accounts_pb2.LoginResponse(
                success=False,
                http_status=401,
                error_message=["Email Verification Required"],
            )

        # Updating user to verified is done in verify_email function
        success, message = verify_email(req.otp, email_verify_id, req.email)

        if success:  # User provided an OTP and it's correct
            return accounts_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user.id,
                user=user.to_dict(),
                otp_required=False,
            )

        return accounts_pb2.LoginResponse(
            success=False,
            http_status=400,
            user_id=-1,
            otp_required=True,
            error_message=[message],
        )

    def Get(self, req: accounts_pb2.GetRequest, context: grpc.ServicerContext) -> accounts_pb2.GetResponse:
        """
        Get allows the retrieval of a user, containing the filters for the users to be returned.

        The filters are optional, at least one filter must be provided.

        The page and limit are optional, with the default page being 0 and the default limit being 50.

        This is intended for admin or self use.
        """
        if req.page < 0:
            req.page = 0
        if req.limit < 1:
            req.limit = 1
        elif req.limit > 50:
            req.limit = 50
        offset = req.page * req.limit

        with get_db() as session:
            users = session.query(User)
            if req.user_id > 0:
                users = users.filter(User.id == req.user_id)
            if req.email != "":
                users = users.filter(User.email == req.email)
            if req.first_name != "":  # Allows partial searching
                users = users.filter(User.first_name.ilike(f"%{req.first_name}%"))
            if req.last_name != "":  # Allows partial searching
                users = users.filter(User.last_name.ilike(f"%{req.last_name}%"))
            if req.email_verified != 0:
                if req.email_verified == 1:
                    users = users.filter(User.email_verified is True)
                else:
                    users = users.filter(User.email_verified is False)
            if req.age_from > 0:  # age from is in years, use 365 as it's days in a year
                users = users.filter(User.date_of_birth <= datetime.now() - timedelta(days=req.age_from * 365))
            if req.age_to > 0:  # age to is in years, use 365 as it's days in a year
                users = users.filter(User.date_of_birth >= datetime.now() - timedelta(days=req.age_to * 365))
            if req.degree_id > 0:
                users = users.filter(User.degree_id == req.degree_id)
            if req.tag_id > 0:
                users = users.join(UserTag).filter(UserTag.tag_id == req.tag_id)
            if req.gender != "":  # Allows lowercase and uppercase
                users = users.filter(User.gender.ilike(f"%{req.gender}%"))
            if req.year_of_study != 0:
                users = users.filter(User.year_of_study == req.year_of_study)

            users = users.offset(offset).limit(req.limit).all()
            users_list = [user.to_dict() for user in users]

            print(users_list)

            return accounts_pb2.GetResponse(
                success=True,
                http_status=200,
                users=users_list,
            )

    def Update(self, req: accounts_pb2.UpdateRequest, context: grpc.ServicerContext) -> accounts_pb2.Response:
        """
        Update allows the updating of a user.

        Send the user object with the total changes to be made. INCLUDE all fields, even if they are not changing.

        This is done so tags can be removed/added.

        It does not return the changes to the user.
        """
        # In more complex system, this would be done more efficiently and cleaner but as this is a prototype
        # it does not require that level of complexity.
        #
        # This would be done as a diff of the user object and the user in the database.
        # With validate functions per field as part of the db user.
        if req.user.id < 1:
            return accounts_pb2.Response(
                success=False,
                http_status=400,
                error_message=["User ID must be greater than 0"],
            )

        with get_db() as session:
            user = session.query(User).filter(User.id == req.user.id).first()
            # Picture URL is done as a separate request so other data won't exist.
            if req.user.picture_url != user.picture_url:
                user.picture_url = req.user.picture_url
                session.commit()
                return accounts_pb2.Response(
                    success=True,
                    http_status=200,
                )

            if req.user.email != user.email:
                return self.update_email(req)

            if req.new_password != "" and not check_password_hash(user.password, req.password) and not req.is_self:
                return accounts_pb2.Response(
                    success=False,
                    http_status=400,  # They are authenticated, but the password is incorrect
                    error_message=["Invalid Password"],
                )

            if req.new_password != "":
                user.password = generate_password_hash(req.new_password)

            if req.user.first_name != user.first_name:
                user.first_name = req.user.first_name
            if req.user.last_name != user.last_name:
                user.last_name = req.user.last_name

            if req.user.degree_id != user.degree_id:
                # While this could be moved into its own function,
                # it's not worth it for a prototype
                degree_client = DegreesClient()
                degree = degree_client.get(degree_pb2.DegreeGetRequest(id=req.user.degree_id))
                if not degree.success:
                    return accounts_pb2.Response(
                        success=False,
                        http_status=400,
                        error_message=['Degree Not Found'],
                    )
                user.degree_id = req.user.degree_id

            dob = datetime.strptime(req.user.date_of_birth, "%d-%m-%Y").date()
            if dob != user.date_of_birth:
                user.date_of_birth = dob

            if req.user.rank != user.rank and not req.is_self:
                user.rank = req.user.rank

            user_tags = session.query(UserTag).filter(UserTag.user_id == user.id).all()
            user_tags = [tag.tag_id for tag in user_tags]
            tags_to_add = [tag for tag in req.user.tags if tag not in user_tags]
            tags_to_remove = [tag for tag in user_tags if tag not in req.user.tags]

            for tag in tags_to_add:
                user_tag = UserTag(user_id=user.id, tag_id=tag)
                session.add(user_tag)

            for tag in tags_to_remove:
                user_tag = session.query(UserTag).filter(UserTag.user_id == user.id, UserTag.tag_id == tag).first()
                session.delete(user_tag)

            session.commit()

        return accounts_pb2.Response(
            success=True,
            http_status=200,
        )

    # noinspection PyMethodMayBeStatic
    def update_email(self, req: accounts_pb2.UpdateRequest) -> accounts_pb2.Response | None:
        """
        Update the email of a user.

        This sends out a verification email to the new email.
        """
        accounts_client = AccountsClient()
        if not req.is_self:
            return None

        if req.skip_email and req.user.email == "":
            return None

        if req.otp:  # OTP is provided
            email_verify_id = accounts_client.get_otp(req.user.id)
            if not email_verify_id:  # If no otp is in cache.
                return accounts_pb2.Response(
                    success=False,
                    http_status=401,
                    error_message=["Email Verification Required"],
                )

            # We don't pass in the email as it's not in the database yet
            success, message = verify_email(req.otp, email_verify_id, "")

            if not success:
                return accounts_pb2.Response(
                    success=False,
                    http_status=400,
                    error_message=[message],
                    otp_required=True,
                )

            with get_db() as session:
                user = session.query(User).filter(User.id == req.user.id).first()
                user.email = req.user.email
                session.commit()

        success, message, otp_seed = send_verification_code_email(req.user.email)

        if success:
            accounts_client.save_otp(req.user.id, str(otp_seed))
            return accounts_pb2.Response(
                success=True,
                http_status=200,
                otp_required=True,
            )
        return accounts_pb2.Response(
            success=False,
            http_status=500,
            error_message=['Error Sending Out Verification Email', message],
        )

    def Delete(self, req: accounts_pb2.DeleteRequest, context: grpc.ServicerContext) -> accounts_pb2.Response:
        """
        Delete allows the deletion of a user.

        There is no confirmation, it's intention is for quick and easy use for the prototype.
        """
        with get_db() as session:
            user = session.query(User).filter(User.id == req.user_id).first()
            if not user:
                return accounts_pb2.Response(
                    success=False,
                    http_status=400,
                    error_message=["User not found"],
                )

            user_tags = session.query(UserTag).filter(UserTag.user_id == user.id).all()

            for user_tag in user_tags:
                session.delete(user_tag)

            session.commit()

            session.delete(user)
            session.commit()

        return accounts_pb2.Response(
            success=True,
            http_status=200,
        )
