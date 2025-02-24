import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import chat_pb2_grpc, chat_pb2


class Service(chat_pb2_grpc.ChatServicer):
    def SendMessage(self, request: chat_pb2.MessageRequest, context: grpc.ServicerContext) -> chat_pb2.MessageResponse:
        return chat_pb2.MessageResponse(success=True, error='', message=f"Hello, {request.message}!")


def serve():
    port = os.environ.get('CHAT_PORT', '50051')
    max_workers = int(os.environ.get('CHAT_MAX_WORKERS', 10))

    print(f"Starting server on port {port} with {max_workers} workers")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    chat_pb2_grpc.add_ChatServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
