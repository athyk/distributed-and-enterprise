import grpc
from backend.common.proto import community_announcement_pb2_grpc, community_announcement_pb2

from backend.community.announcements.create import create_announcement
from backend.community.announcements.view import get_community_announcements, get_specified_community_announcement, get_global_community_announcements
from backend.community.announcements.edit import edit_announcement
from backend.community.announcements.delete import delete_announcement


class Community_Announcement_Service(community_announcement_pb2_grpc.CommunityAnnouncementServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def CommunityCreateAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementCreateRequest, context: grpc.ServicerContext) -> community_announcement_pb2.CommunityAnnouncementResponse:
        '''
        This function verifies incoming data and creates a new community announcement.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("CommunityCreateAnnouncement Request Made:")
        print(request)

        success, message = create_announcement(request.community_id, request.user_id, request.title, request.description, list(request.tags))
        http_code = 201

        if not success:
            http_code = 400
        
        return community_announcement_pb2.CommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message)
    

    def CommunityViewSelectAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementViewSelectRequest, context: grpc.ServicerContext) -> community_announcement_pb2.AllCommunityAnnouncementResponse:
        '''
        This function verifies incoming data and fetches a select number of community announcements.
        If any errors arise then relevant error messages are returned.
        '''
    
        print("CommunityViewSelectAnnouncement Request Made:")
        print(request)

        success, message, announcement_list = get_community_announcements(request.community_id, request.user_id, request.offset, request.limit)
        http_code = 200

        announcements = []

        if not success:
            http_code = 400

        else:
            for announcement in announcement_list:
                announce_object = community_announcement_pb2.CommunityAnnouncementData(
                    id=announcement.get('id'),
                    title=announcement.get('title'),
                    description=announcement.get('description'),
                    tags=announcement.get('tags'),
                    user_id=announcement.get('user_id'),
                    uploaded=announcement.get('uploaded'),
                    edit_user_id=announcement.get('edit_user_id'),
                    edit_uploaded=announcement.get('edit_uploaded')
                )

                announcements.append(announce_object)
        
        return community_announcement_pb2.AllCommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message, announcements=announcements)
    

    def CommunityUpdateAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementUpdateRequest, context: grpc.ServicerContext) -> community_announcement_pb2.CommunityAnnouncementResponse:
        '''
        This function verifies incoming data and updates a community announcement.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("CommunityUpdateAnnouncement Request Made:")
        print(request)

        success, message = edit_announcement(request.announcement_id, request.community_id, request.user_id, request.title, request.description, list(request.tags))
        http_code = 201

        if not success:
            http_code = 400
        
        return community_announcement_pb2.CommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message)
    

    def CommunityDeleteAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementDeleteRequest, context: grpc.ServicerContext) -> community_announcement_pb2.CommunityAnnouncementResponse:
        '''
        This function verifies incoming data and updates a community announcement.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("CommunityDeleteAnnouncement Request Made:")
        print(request)

        success, message = delete_announcement(request.announcement_id, request.community_id, request.user_id)
        http_code = 201

        if not success:
            http_code = 400
        
        return community_announcement_pb2.CommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message)


    def CommunityViewSelectOneAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementViewSelectOneRequest, context: grpc.ServicerContext) -> community_announcement_pb2.SingleCommunityAnnouncementResponse:
        '''
        This function verifies incoming data and fetches a select number of community announcements.
        If any errors arise then relevant error messages are returned.
        '''

        print("CommunityViewSelectOneAnnouncement Request Made:")
        print(request)

        success, message, announcement = get_specified_community_announcement(request.announcement_id, request.community_id, request.user_id)
        http_code = 200

        announce_object = None

        if not success:
            http_code = 400

            return community_announcement_pb2.SingleCommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message)

        else:
            announce_object = community_announcement_pb2.CommunityAnnouncementData(
                id=announcement.get('id'),
                title=announcement.get('title'),
                description=announcement.get('description'),
                tags=announcement.get('tags'),
                user_id=announcement.get('user_id'),
                uploaded=announcement.get('uploaded'),
                edit_user_id=announcement.get('edit_user_id'),
                edit_uploaded=announcement.get('edit_uploaded')
            )
        
            return community_announcement_pb2.SingleCommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message, announcement=announce_object)


    def CommunityViewGlobalAnnouncement(self, request: community_announcement_pb2.CommunityAnnouncementGlobalRequest, context: grpc.ServicerContext) -> community_announcement_pb2.GlobalCommunityAnnouncementResponse:
        '''
        This function verifies incoming data and fetches a select number of announcements.
        '''
    
        print("CommunityViewGlobalAnnouncement Request Made:")
        print(request)

        success, message, announcement_list = get_global_community_announcements(request.offset, request.limit)
        http_code = 200

        announcements = []

        if not success:
            http_code = 400

        else:
            for announcement in announcement_list:
                announce_object = community_announcement_pb2.GlobalCommunityAnnouncementData(
                    id=announcement.get('id'),
                    community_id=announcement.get('community_id'),
                    title=announcement.get('title'),
                    description=announcement.get('description'),
                    tags=announcement.get('tags'),
                    user_id=announcement.get('user_id'),
                    uploaded=announcement.get('uploaded'),
                    edit_user_id=announcement.get('edit_user_id'),
                    edit_uploaded=announcement.get('edit_uploaded')
                )

                announcements.append(announce_object)
        
        return community_announcement_pb2.GlobalCommunityAnnouncementResponse(success=success, http_status=http_code, error_message=message, global_announcements=announcements)
