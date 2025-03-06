import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import authentication_pb2_grpc, data_fetching_pb2_grpc
from backend.auth.database.database import engine, Base, confirm_database_exists

from backend.auth.services.authentication_service import AuthenticationService, DataFetchingService


def serve():
    port = os.environ.get('AUTH_PORT', '50053')
    max_workers = int(os.environ.get('AUTH_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    authentication_pb2_grpc.add_AuthenticationServicer_to_server(AuthenticationService(), server)
    data_fetching_pb2_grpc.add_DataFetchServicer_to_server(DataFetchingService(), server)
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
