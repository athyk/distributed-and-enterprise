import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import authentication_pb2_grpc, authentication_pb2


class Authentication(authentication_pb2_grpc.AuthServicer):
    def RegisterUser(self, request: authentication_pb2.RegistrationRequest, context: grpc.ServicerContext) -> authentication_pb2.AuthenticationResponse:
        
        # add functions here
        
        return authentication_pb2.AuthenticationResponse(
            success=True,
            http_status=200,
            error_message=[],
            user_id=-1
        )

    def LoginUser(self, request: authentication_pb2.LoginRequest, context: grpc.ServicerContext) -> authentication_pb2.AuthenticationResponse:
        
        # add functions here
        
        return authentication_pb2.AuthenticationResponse(
            success=True,
            http_status=200,
            error_message=[],
            user_id=-1
        )

    def SendEmailRequest(self, request: authentication_pb2.EmailAuthRequest, context: grpc.ServicerContext) -> authentication_pb2.EmailAuthSent:
        
        # add functions here
        
        return authentication_pb2.EmailAuthSent(
            sent=True,
            error_message=[]
        )

    def EmailConfirmationRequest(self, request: authentication_pb2.EmailAuthVerify, context: grpc.ServicerContext) -> authentication_pb2.EmailVerifiedResponse:
        
        # add functions here
        
        return authentication_pb2.EmailVerifiedResponse(
            verified=True,
            error_message=[]
        )






def serve():
    port = os.environ.get('AUTH_PORT', '50053')
    max_workers = int(os.environ.get('AUTH_MAX_WORKERS', 10))

    print(f"Starting server on port {port} with {max_workers} workers")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    authentication_pb2_grpc.add_AuthenticationServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
