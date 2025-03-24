import os
import grpc
from concurrent import futures

from backend.tag.services.rpc import TagServicer
# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import tag_pb2_grpc
from backend.tag.database.database import engine, Base, confirm_database_exists
from backend.common.services import AccountsClient, TagsClient, DegreesClient
from backend.common.services.community.community import CommunityClient
from backend.common.services.community.announcement import CommunityAnnouncementClient
from backend.common.services.community.joins import CommunityJoinsClient
from backend.common.services.community.event import CommunityEventClient
from backend.common.services.community.member import CommunityMemberClient

os.environ["GRPC_DNS_RESOLVER"] = "native"


def serve():
    port = os.environ.get('TAG_PORT', '50054')
    max_workers = int(os.environ.get('TAG_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    tag_pb2_grpc.add_TagsServicer_to_server(TagServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print('\n--------------------------- Server Started --------------------------\n')

    print('----------------- Internal Server Setup Initialising ----------------\n')

    print("Initialising Helper Clients")

    AccountsClient.initialise(
        "account-service:" + os.environ.get('ACC_PORT', '50053'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    TagsClient.initialise(
        "tag-service:" + os.environ.get('TAG_PORT', '50054'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    DegreesClient.initialise(
        "degree-service:" + os.environ.get('DEGREE_PORT', '50055'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    CommunityClient.initialise(
        "community-service:" + os.environ.get('COMMUNITY_PORT', '50052'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    CommunityAnnouncementClient.initialise(
        "community-service:" + os.environ.get('COMMUNITY_PORT', '50052'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    CommunityJoinsClient.initialise(
        "community-service:" + os.environ.get('COMMUNITY_PORT', '50052'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    CommunityEventClient.initialise(
        "community-service:" + os.environ.get('COMMUNITY_PORT', '50052'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    CommunityMemberClient.initialise(
        "community-service:" + os.environ.get('COMMUNITY_PORT', '50052'),
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
