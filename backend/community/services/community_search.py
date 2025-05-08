import grpc
from backend.common.proto import community_searching_pb2_grpc, community_searching_pb2

from backend.community.search.search import search_for_community



class Community_Searching_Service(community_searching_pb2_grpc.CommunitySearchingServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def CommunitySearch(self, request: community_searching_pb2.Filter, context: grpc.ServicerContext) -> community_searching_pb2.CommunityFilter:
        '''
        This function verifies incoming data and creates a new community.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("CommunitySearch Request Made:")
        print(request)

        try:

            success, http_code, message, filter = search_for_community(
                request.offset,
                request.limit,
                request.user_id,
                request.is_with,
                request.name,
                request.public,
                request.minimum_members,
                list(request.tags),
                list(request.degrees)
            )
        
        except Exception as e:
            print(e)

        print(filter)

        status = community_searching_pb2.RequestResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )

        filtered = []

        for community in filter:
            public = 2

            if community.get('public') == 1:
                print('public')
                public = 1
            
            filtered.append(community_searching_pb2.CommunityData(
                id=community.get('id', 0),
                name=community.get('name', ''),
                description=community.get('description', ''),
                public_community=public,
                member_count=community.get('member_count', 0),
                tags=community.get('tags', []),
                degrees=community.get('degrees', []),
            ))

        print('-----')

        print(filtered)
        
        return community_searching_pb2.CommunityFilter(status=status, communities=filtered)
