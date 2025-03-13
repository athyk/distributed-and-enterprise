import traceback
from datetime import datetime, UTC
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
        email_verify, email_error = verify_string(req.email, 4, 255)  # Cannot exceed 255 rfc3696
        password_verify, password_error = verify_string(req.password, 8, inf)
        first_name_verify, first_name_error = verify_string(req.first_name, 1, inf)
        last_name_verify, last_name_error = verify_string(req.last_name, 1, inf)
        gender_verify, gender_error = verify_string(req.gender, 4, 12)
        degree_id_verify, degree_id_error = verify_integer(req.degree_id, 1, inf)
        year_of_study_verify, year_of_study_error = verify_integer(req.year_of_study, 1, 9)
        tag_verify, tag_error = verify_list(list(req.tags), 0, 5)
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

        success, message, otp_seed = send_verification_code_email(req.email)

        if success:
            return accounts_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user.id,
                otp_required=True,
                email_id=str(otp_seed),
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
        email_verify, email_error = verify_string(req.email, 4, 255)  # Cannot exceed 255 rfc3696
        password_verify, password_error = verify_string(req.password, 8, inf)

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
        # TODO: Get User
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, req: accounts_pb2.UpdateRequest, context: grpc.ServicerContext) -> accounts_pb2.Response:
        """
        Update allows the updating of a user.

        Send the user object with the total changes to be made. INCLUDE all fields, even if they are not changing.

        It does not return the changes to the user.
        """
        # TODO: Update User
        # TODO: Update user tags
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, req: accounts_pb2.DeleteRequest, context: grpc.ServicerContext) -> accounts_pb2.Response:
        """
        Delete allows the deletion of a user.
        """
        # TODO: Delete User
        # TODO: Delete user tags
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
