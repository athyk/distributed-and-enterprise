import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import community_pb2_grpc, community_announcement_pb2_grpc, community_joins_pb2_grpc
from backend.common.services import AccountsClient, TagsClient, DegreesClient
from backend.common.services.community.community import CommunityClient
from backend.common.services.community.announcement import CommunityAnnouncementClient
from backend.common.services.community.joins import CommunityJoinsClient

from backend.community.database.database import engine, Base, confirm_database_exists

# All community services that will be run goes here
from backend.community.services.community_crud import Community_CRUD_Service
from backend.community.services.community_announcements import Community_Announcement_Service
from backend.community.services.community_joins import Community_Joins_Service

def serve():
    port = os.environ.get('COMMUNITY_PORT', '50052')
    max_workers = int(os.environ.get('COMMUNITY_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[('grpc.max_message_length', 50 * 1024 * 1024)]
    )

    community_pb2_grpc.add_CommunityServicer_to_server(Community_CRUD_Service(), server)
    print('Service Added: CRUD-Service')

    community_announcement_pb2_grpc.add_CommunityAnnouncementServicer_to_server(Community_Announcement_Service(), server)
    print('Service Added: Announcement-Service')

    community_joins_pb2_grpc.add_CommunityJoinsServicer_to_server(Community_Joins_Service(), server)
    print('Service Added: Joins-Service')

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

    confirm_database_exists()

    print('\nCreating All Tables')
    Base.metadata.create_all(engine)
    print('Tables Created')

    print('\n------------------ Internal Server Setup Completed ------------------')

    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
