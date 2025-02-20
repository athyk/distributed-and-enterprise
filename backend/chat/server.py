import os
import grpc
from concurrent import futures

from backend.common.proto import chat_pb2_grpc,chat_pb2


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


if __name__ == '__main__': # pragma: no cover
    serve()
