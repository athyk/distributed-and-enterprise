import grpc
from backend.common.proto import community_member_management_pb2, community_member_management_pb2_grpc

from backend.community.member.promote import promote_user
from backend.community.member.demote import demote_user
from backend.community.member.ban import ban_user
from backend.community.member.all_members import get_all_community_users


class Community_Member_Management_Service(community_member_management_pb2_grpc.MemberManagementServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def PromoteUser(self, request: community_member_management_pb2.UserRequest, context: grpc.ServicerContext) -> community_member_management_pb2.MemberActionResponse:
        '''
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("PromoteUser Request Made:")
        print(request)

        success, http_code, message = promote_user(request.community_id, request.user_id, request.action_user_id)
        
        return community_member_management_pb2.MemberActionResponse(success=success, http_status=http_code, error_message=message)
    

    def DemoteUser(self, request: community_member_management_pb2.UserRequest, context: grpc.ServicerContext) -> community_member_management_pb2.MemberActionResponse:
        '''
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("DemoteUser Request Made:")
        print(request)

        success, http_code, message = demote_user(request.community_id, request.user_id, request.action_user_id)
        
        return community_member_management_pb2.MemberActionResponse(success=success, http_status=http_code, error_message=message)


    def BanUser(self, request: community_member_management_pb2.UserRequest, context: grpc.ServicerContext) -> community_member_management_pb2.MemberActionResponse:
        '''
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("BanUser Request Made:")
        print(request)

        success, http_code, message = ban_user(request.community_id, request.user_id, request.action_user_id)
        
        return community_member_management_pb2.MemberActionResponse(success=success, http_status=http_code, error_message=message)
    
    def GetAllCommunityUser(self, request: community_member_management_pb2.UserRequest, context: grpc.ServicerContext) -> community_member_management_pb2.MemberActionResponse:
        '''
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("GetAllCommunityUser Request Made:")
        print(request)

        success, http_code, message, data = get_all_community_users(request.community_id, request.user_id)
        
        return community_member_management_pb2.AllUsers(success=success, http_status=http_code, error_message=message, users=data)
