import grpc
from backend.common.proto import community_pb2_grpc, community_pb2

from backend.community.crud.create import create_community
from backend.community.crud.view import get_community_data
from backend.community.crud.update import update_community
from backend.community.crud.delete import delete_community


class Community_CRUD_Service(community_pb2_grpc.CommunityServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def CommunityCreate(self, request: community_pb2.CommunityCreateRequest, context: grpc.ServicerContext) -> community_pb2.CommunityIDResponse:
        """
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        """
        
        print("CommunityCreate Request Made:")
        print(request)

        success, id, message = create_community(request.name, request.description, request.public, list(request.tags), list(request.degrees), request.user_id)
        http_code = 201

        if not success:
            http_code = 400
        
        return community_pb2.CommunityIDResponse(success=success, http_status=http_code, error_message=message, id=id)

    def CommunityView(self, request: community_pb2.CommunityViewRequest, context: grpc.ServicerContext) -> community_pb2.CommunityDataResponse:
        """
        This function verifies incoming data and fetches the specified community data.
        If any errors arise then relevant error messages are returned.
        """
        
        print("CommunityView Request Made:")
        print(request)

        success, message, name, description, public, tag, degree = get_community_data(request.id)
        http_code = 200

        if not success:
            http_code = 400

        return community_pb2.CommunityDataResponse(
            success=success,
            http_status=http_code,
            error_message=message,
            name=name,
            description=description,
            public_community=public,
            tags=tag,
            degrees=degree
            )

    def CommunityUpdate(self, request: community_pb2.CommunityUpdateRequest, context: grpc.ServicerContext) -> community_pb2.BasicCommunityResponse:
        """
        This function verifies incoming data and updates the specified community data.
        If any errors arise then relevant error messages are returned.
        """
        
        print("CommunityUpdate Request Made:")
        print(request)

        success, message = update_community(request.id, request.name, request.description, request.public, list(request.tags), list(request.degrees), request.user_id)
        http_code = 200

        if not success:
            http_code = 400

        return community_pb2.BasicCommunityResponse(success=success, http_status=http_code, error_message=message)

    def CommunityDelete(self, request: community_pb2.CommunityDeleteRequest, context: grpc.ServicerContext) -> community_pb2.BasicCommunityResponse:
        """
        This function verifies incoming data and deletes the specified community.
        If any errors arise then relevant error messages are returned.
        """
        
        print("CommunityDelete Request Made:")
        print(request)

        success, message = delete_community(request.id, request.user_id)
        http_code = 200

        if not success:
            http_code = 400

        return community_pb2.BasicCommunityResponse(success=success, http_status=http_code, error_message=message)
