import os
import grpc
from concurrent import futures

from backend.accounts.services.auth import AccountsServicer
from backend.accounts.services.posts import AccountsPostsServicer
# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import accounts_pb2_grpc
from backend.common.proto import account_post_pb2_grpc
from backend.accounts.database.database import engine, Base, confirm_database_exists
from backend.common.services import AccountsClient, TagsClient, DegreesClient
from backend.common.services.account_posts import AccountPostsClient
from backend.common.services.community.community import CommunityClient
from backend.common.services.community.announcement import CommunityAnnouncementClient
from backend.common.services.community.joins import CommunityJoinsClient
from backend.common.services.community.event import CommunityEventClient
from backend.common.services.community.member import CommunityMemberClient
from backend.common.services.community.search import CommunitySearchingClient

os.environ["GRPC_DNS_RESOLVER"] = "native"


def serve():
    port = os.environ.get('AUTH_PORT', '50053')
    max_workers = int(os.environ.get('AUTH_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    # While originally a dedicated posts service would be most appropriate, since community announcements
    # is similar to posts just tied to a community is located within the community service.
    #
    # It would then make sense to make the account posts service located within accounts so that
    # for future expansion after the prototype they can then all be moved into a posts service.
    accounts_pb2_grpc.add_AccountsServicer_to_server(AccountsServicer(), server)
    account_post_pb2_grpc.add_AccountPostsServicer_to_server(AccountsPostsServicer(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print('\n--------------------------- Server Started --------------------------\n')

    print('----------------- Internal Server Setup Initialising ----------------\n')

    print("Initialising Helper Clients")
    AccountsClient.initialise(
        "account-service:" + os.environ.get('ACC_PORT', '50053'),
        os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    )

    AccountPostsClient.initialise(
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

    CommunitySearchingClient.initialise(
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
