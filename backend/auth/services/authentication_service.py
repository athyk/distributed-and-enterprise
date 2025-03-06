import grpc

from backend.common.proto import authentication_pb2_grpc, authentication_pb2
from backend.common.proto import data_fetching_pb2_grpc, data_fetching_pb2

from backend.auth.login_files.login import user_login
from backend.auth.login_files.register import register_user

from backend.auth.data_fetching.get_degrees import get_degrees
from backend.auth.data_fetching.get_tags import get_tags

from google.protobuf import empty_pb2


class AuthenticationService(authentication_pb2_grpc.AuthenticationServicer):
    def RegisterUser(self, request: authentication_pb2.RegistrationRequest, context: grpc.ServicerContext) -> authentication_pb2.AuthenticationResponse:
        """
        This grpc request gets the relevant data and registers the user into the website.
        If any errors arise then relevant error messages are returned.
        """

        print("RegisterUser Request Made:")
        print(request)

        success, user_id, error_message = register_user(
            request.email,
            request.password,
            request.first_name,
            request.last_name,
            request.dob,
            request.gender,
            request.degree,
            request.year_of_study,
            request.grad_year,
            list(request.tag)
        )

        http_code = 201

        if not success:
            http_code = 400

        return authentication_pb2.AuthenticationResponse(
            success=success,
            http_status=http_code,
            error_message=error_message,
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
    

class DataFetchingService(data_fetching_pb2_grpc.DataFetchServicer):
    def FetchDegrees(self, request: empty_pb2.Empty, context: grpc.ServicerContext) -> data_fetching_pb2.DataListResponse:
        """
        This grpc request verifies the users account with the code provided by the user.
        If any errors arise then relevant error messages are returned.
        """

        print("FetchDegrees Request Made:")
        print(request)

        degrees = get_degrees()
        
        return data_fetching_pb2.DataListResponse(
            success=True,
            http_status=200,
            error_message=[],
            data=degrees
        )
    

    def FetchTags(self, request: empty_pb2.Empty, context: grpc.ServicerContext) -> data_fetching_pb2.DataListResponse:
        """
        This grpc request verifies the users account with the code provided by the user.
        If any errors arise then relevant error messages are returned.
        """

        print("FetchTags Request Made:")
        print(request)

        tags = get_tags()
        
        return data_fetching_pb2.DataListResponse(
            success=True,
            http_status=200,
            error_message=[],
            data=tags
        )
