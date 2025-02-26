import os
import grpc
from concurrent import futures

# If paths are not resolved correctly, you may copy the files `chat_pb2.py`, `chat_pb2_grpc.py`, and `chat_pb2.pyi`
# to this folder and replace the below import statement. Ensure those moved files are not committed to the repository.
#
# Alternatively you may convert the following for use on your operating system: PYTHONPATH=$(pwd)/backend/common/proto
# But if any issues happen, use the docker compose command to run the server.
from backend.common.proto import community_pb2_grpc, community_pb2


from backend.community.database.database import engine, Base, confirm_database_exists




from backend.community.crud.create import create_community


class Service(community_pb2_grpc.CommunityServicer):
    def CommunityCreate(self, request: community_pb2.CommunityCreateRequest, context: grpc.ServicerContext) -> community_pb2.CommunityIDResponse:
        
        print("CommunityCreate Request Made:")
        print(request)

        success, id, message = create_community(request.name, request.description, request.public, list(request.tags), list(request.degrees), request.user_id)

        print(success, id, message)

        print(message)
        
        return community_pb2.CommunityIDResponse(success=success, http_status=200, error_message=message, id=id)



def serve():
    port = os.environ.get('COMMUNITY_PORT', '50051')
    max_workers = int(os.environ.get('COMMUNITY_MAX_WORKERS', 10))

    print('--------------------------- Server Starting -------------------------\n')

    print(f'Port: {port}')
    print(f'Max Workers Assigned: {max_workers}')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    community_pb2_grpc.add_CommunityServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print('\n--------------------------- Server Started --------------------------\n')

    print('----------------- Internal Server Setup Initialising ----------------\n')

    confirm_database_exists()

    print('Creating All Tables')
    Base.metadata.create_all(engine)
    print('Tables Created')

    print('\n------------------ Internal Server Setup Completed ------------------')

    server.wait_for_termination()


# Below allows running the server directly using `python server.py` although not recommended.
if __name__ == '__main__':  # pragma: no cover
    serve()
