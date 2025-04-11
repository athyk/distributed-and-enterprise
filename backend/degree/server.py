import os
import grpc
from concurrent import futures

from backend.degree.services.rpc import DegreeServicer
# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import degree_pb2_grpc
from backend.degree.database.database import engine, Base, confirm_database_exists
from backend.common.services import DegreesClient

os.environ["GRPC_DNS_RESOLVER"] = "native"


def serve():
    port = os.environ.get('DEGREE_PORT', '50055')
    max_workers = int(os.environ.get('DEGREE_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    degree_pb2_grpc.add_DegreesServicer_to_server(DegreeServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print('\n--------------------------- Server Started --------------------------\n')

    print('----------------- Internal Server Setup Initialising ----------------\n')

    print("Initialising Helper Client")

    # Degrees only relies on itself, as it's a standalone service.
    #
    # If it did data validation such as checking if a user exists, it would need to initialise the AccountsClient.
    # But as it only handles degrees, it doesn't need to do that.
    DegreesClient.initialise(
        "degree-service:" + os.environ.get('DEGREE_PORT', '50055'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    confirm_database_exists()

    print('\nCreating All Tables')
    Base.metadata.create_all(engine)
    print('Tables Created')

    print('\n------------------ Internal Server Setup Completed ------------------')

    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
