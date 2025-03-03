from datetime import datetime, UTC

import grpc
from werkzeug.security import generate_password_hash, check_password_hash

from backend.auth.database.database import get_db
from backend.auth.database.models import User
from backend.auth.logic.local_functions import generate_id
# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import auth_pb2_grpc, auth_pb2


class AuthService(auth_pb2_grpc.AuthServicer):
    def UserRegister(self, req: auth_pb2.RegistrationRequest,
                     context: grpc.ServicerContext) -> auth_pb2.LoginResponse:
        """
        Allows the registration of a user.

        Links to SCRUM-100
        """

        # Validate type specific inputs, since dates are in seconds, they must be converted to datetime objects.
        # This couldn't have been done in the client/utils.

        try:
            dob = datetime.fromtimestamp(req.dob, UTC)
            grad_date = datetime.fromtimestamp(req.grad_date, UTC)
        except Exception:  # May throw OverflowError, OSError, or ValueError
            return auth_pb2.LoginResponse(
                success=False,
                http_status=400,
                error_message=["Invalid date(s) is not valid."],
            )

        with get_db() as session:
            user: User | None = session.query(User).filter(User.email == req.email).first()

            if user:
                return auth_pb2.LoginResponse(
                    success=False,
                    http_status=400,
                    error_message=["Email already in use."],
                )

            # generate id first, probability of at least one collision is 2.71 quintillion
            # https://en.wikipedia.org/wiki/Universally_unique_identifier#Collisions
            #
            # no need to check for collisions as the probability is so low, it doesn't matter in the prototype.
            user_id, error = generate_id()

            if error:
                return auth_pb2.LoginResponse(
                    success=False,
                    http_status=500,
                    error_message=["An error occurred while generating the user ID."],
                )

            # Use scrypt to hash the password, it's more secure than bcrypt and less complicated
            # for a prototype than argon2.
            hashed_password = generate_password_hash(req.password)

            user = User(
                email=req.email,
                password=hashed_password,
                full_name=req.first_name + " " + req.last_name,
                first_name=req.first_name,
                last_name=req.last_name,
                nickname=req.nickname,
                date_of_birth=dob,
                gender=req.gender,
                degree=req.degree,
                year_of_study=req.year_of_study,
                grad_date=grad_date,
                # no picture_url as that's done in user update.
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )

            user.id = user_id

            session.add(user)
            session.commit()

            # it's now expected that the user verifies their email address
            # and submits an OTP through UserLoginVerification
            return auth_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user_id,
                otp_required=True,
            )

    def UserLogin(self, req: auth_pb2.LoginRequest, context: grpc.ServicerContext) -> auth_pb2.LoginResponse:
        """
        Allows the login of a user.

        Links to SCRUM-100
        """
        with get_db() as session:
            user: User = session.query(User).filter(User.email == req.email).first()

            if not user:
                return auth_pb2.LoginResponse(
                    success=False,
                    http_status=400,
                    error_message=["Invalid email or password."],
                )

            if not check_password_hash(user.password, req.password):
                return auth_pb2.LoginResponse(
                    success=False,
                    http_status=400,
                    error_message=["Invalid email or password."],
                )

            # only for development, otherwise, the email would be sent.
            if req.skip_email:
                return auth_pb2.LoginResponse(
                    success=True,
                    http_status=200,
                    user_id=user.id,
                    user=user.to_dict(),
                    otp_required=False,
                )

            # If the user hasn't verified their email, they can't login.
            # incase the email was not sent, through this request it will be resent

            # In here email 2fa code can be generated, sent, and stored for later verification
            # TODO: add code to cache for later use for email otp, use redis

            return auth_pb2.LoginResponse(
                success=True,
                http_status=200,
                user_id=user.id,
                otp_required=True,
            )

    def UserLoginVerification(self, req: auth_pb2.LoginVerificationRequest,
                              context: grpc.ServicerContext) -> auth_pb2.LoginVerificationResponse:
        """
        Allows the verification of a user.

        This can be /login/verify or /register/verify depending on the request.

        Links to SCRUM-100
        """
        with get_db() as session:
            user: User = session.query(User).filter(User.id == req.user_id).first()

            if not user:
                return auth_pb2.LoginVerificationResponse(
                    success=False,
                    http_status=400,
                    error_message=["User not found."],
                )

            # TODO: Check if OTP is a totp code
            if req.otp != "123456":  # TODO: Check if the OTP is correct, use redis, and ensure_valid_otp in local_functions
                return auth_pb2.LoginVerificationResponse(
                    success=False,
                    http_status=400,
                    error_message=["Invalid OTP."],
                )

            return auth_pb2.LoginVerificationResponse(
                success=True,
                http_status=200,
                user=user.to_dict(),
            )

    def UserGet(self, request: auth_pb2.GetRequest, context: grpc.ServicerContext) -> auth_pb2.GetResponse:
        """
        Allows the retrieval of a user, containing the filters for the users to be returned.

        The filters are optional, at least one filter must be provided.

        The page and limit are optional, with the default page being 0 and the default limit being 50.

        Links to SCRUM-159
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserUpdate(self, request: auth_pb2.UpdateRequest, context: grpc.ServicerContext) -> auth_pb2.Response:
        """
        Allows the updating of a user.

        Send the user object with the total changes to be made. INCLUDE all fields, even if they are not changing.

        It does not return the changes to the user.

        Links to SCRUM-159
        """
        # TODO: Handle OTP verification

        # TODO: Handle password change and rehashing

        # TODO: Handle email change, and new email verification

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserDelete(self, request: auth_pb2.DeleteRequest, context: grpc.ServicerContext) -> auth_pb2.Response:
        """
        allows the deletion of a user.

        Links to SCRUM-159
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
