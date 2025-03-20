import grpc
from backend.common.proto import community_joins_pb2, community_joins_pb2_grpc

from backend.community.joins.join import add_user_to_community
from backend.community.joins.leave import remove_user_in_community
from backend.community.joins.within import is_user_in_community
from backend.community.joins.invite import invite_user_to_community


class Community_Joins_Service(community_joins_pb2_grpc.CommunityJoinsServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def JoinCommunity(self, request: community_joins_pb2.CommunityActionRequest, context: grpc.ServicerContext) -> community_joins_pb2.CommunityActionResponse:
        '''
        This function verifies incoming data and adds a user to the community.
        If the community is private, they will request access.
        If the private community has already invited the user, they are added.
        If they are banned, they can not join the community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("JoinCommunity Request Made:")
        print(request)

        success, http_code, message = add_user_to_community(request.community_id, request.user_id)
        
        return community_joins_pb2.CommunityActionResponse(success=success, http_status=http_code, error_message=message)
    

    def LeaveCommunity(self, request: community_joins_pb2.CommunityActionRequest, context: grpc.ServicerContext) -> community_joins_pb2.CommunityActionResponse:
        '''
        This function verifies incoming data and adds a user to the specified community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("LeaveCommunity Request Made:")
        print(request)

        success, http_code, message = remove_user_in_community(request.community_id, request.user_id)
        
        return community_joins_pb2.CommunityActionResponse(success=success, http_status=http_code, error_message=message)
    

    def WithCommunity(self, request: community_joins_pb2.CommunityActionRequest, context: grpc.ServicerContext) -> community_joins_pb2.CommunityActionResponse:
        '''
        This function verifies incoming data and adds a user to the specified community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("WithCommunity Request Made:")
        print(request)

        success, http_code, message = is_user_in_community(request.community_id, request.user_id)
        
        return community_joins_pb2.CommunityActionResponse(success=success, http_status=http_code, error_message=message)
    

    def InviteToCommunity(self, request: community_joins_pb2.CommunityInviteRequest, context: grpc.ServicerContext) -> community_joins_pb2.CommunityActionResponse:
        '''
        This function verifies incoming data and adds a user to the specified community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("InviteToCommunity Request Made:")
        print(request)

        success, http_code, message = invite_user_to_community(request.community_id, request.user_id, request.invite_user_id)
        
        return community_joins_pb2.CommunityActionResponse(success=success, http_status=http_code, error_message=message)
