import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import authentication_pb2_grpc, authentication_pb2
from backend.auth.database.database import engine, Base, confirm_database_exists

from backend.auth.login_files.login import user_login
from backend.auth.login_files.register import register_user


class AuthenticationService(authentication_pb2_grpc.AuthServicer):
    def RegisterUser(self, request: authentication_pb2.RegistrationRequest, context: grpc.ServicerContext) -> authentication_pb2.AuthenticationResponse:
        """
        This grpc request gets the relevant data and registers the user into the website.
        If any errors arise then relevant error messages are returned.
        """

        print("RegisterUser Request Made:")
        print(request)

        success, user_id, error_messsage = register_user(
            request.email,
            request.password,
            request.first_name,
            request.last_name,
            request.dob,
            request.gender,
            request.degree,
            request.year_of_study,
            request.grad_year,
            request.tag
        )

        http_code = 201

        if not success:
            http_code = 400

        return authentication_pb2.AuthenticationResponse(
            success=success,
            http_status=http_code,
            error_message=error_messsage,
            user_id=user_id
        )


    def LoginUser(self, request: authentication_pb2.LoginRequest, context: grpc.ServicerContext) -> authentication_pb2.AuthenticationResponse:
        """
        This grpc request gets the relevant data and logs the user into the website.
        If any errors arise then relevant error messages are returned.
        """

        print("LoginUser Request Made:")
        print(request)

        success, user_id, error_messsage = user_login(request.email, request.password)

        http_code = 201

        if not success:
            http_code = 400

        return authentication_pb2.AuthenticationResponse(
            success=success,
            http_status=http_code,
            error_message=error_messsage,
            user_id=user_id
        )

    def SendEmailRequest(self, request: authentication_pb2.EmailAuthRequest, context: grpc.ServicerContext) -> authentication_pb2.EmailAuthSent:
        """
        This grpc request sends an email to the user for them to verify their account.
        If any errors arise then relevant error messages are returned.
        """

        print("SendEmailRequest Request Made:")
        print(request)

        # add functions here
        
        return authentication_pb2.EmailAuthSent(
            sent=True,
            error_message=[]
        )

    def EmailConfirmationRequest(self, request: authentication_pb2.EmailAuthVerify, context: grpc.ServicerContext) -> authentication_pb2.EmailVerifiedResponse:
        """
        This grpc request verifies the users account with the code provided by the user.
        If any errors arise then relevant error messages are returned.
        """

        print("EmailConfirmationRequest Request Made:")
        print(request)

        # add functions here
        
        return authentication_pb2.EmailVerifiedResponse(
            verified=True,
            error_message=[]
        )


def serve():
    port = os.environ.get('AUTH_PORT', '50053')
    max_workers = int(os.environ.get('AUTH_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    authentication_pb2_grpc.add_AuthenticationServicer_to_server(AuthenticationService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print('\n--------------------------- Server Started --------------------------\n')

    print('----------------- Internal Server Setup Initialising ----------------\n')

    confirm_database_exists()

    print('\nCreating All Tables')
    Base.metadata.create_all(engine)
    print('Tables Created')

    print('\n------------------ Internal Server Setup Completed ------------------')

    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
