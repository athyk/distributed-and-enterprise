import grpc
from concurrent import futures
import time

import service_pb2
import service_pb2_grpc

from run_func import func


# gRPC service implementation
class MyServiceServicer(service_pb2_grpc.MyServiceServicer):
    def GetUser(self, request, context):

        func()

        return service_pb2.UserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep the server alive
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()