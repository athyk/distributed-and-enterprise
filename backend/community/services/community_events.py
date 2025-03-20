import grpc
from backend.common.proto import community_event_pb2_grpc, community_event_pb2

from backend.community.events.create import create_event
from backend.community.events.view import view_community_events, view_global_events, view_one_event
from backend.community.events.edit import edit_event
from backend.community.events.delete import delete_event


def format_events(events: list) -> list:
    """
    This function takes the list of events and formats it into grpc expected data
    """

    lst = []

    for event in events:
        try:
            event_grpc = community_event_pb2.ViewEvent(
                id=event.get('id'),
                community_id=event.get('community_id'),
                title=event.get('title'),
                description=event.get('description'),
                location=event.get('location'),
                datetime=event.get('datetime'),
                duration=event.get('duration')
            )

            if event.get('latitude') is not None and event.get('longitude') is not None:
                event_grpc.latitude = event.get('latitude')
                event_grpc.longitude = event.get('longitude')

            lst.append(event_grpc)

        except Exception as e:
            print('---')
            print(e)
            print('---')

    return lst


class Community_Event_Service(community_event_pb2_grpc.CommunityEventServicer):
    """
    This class holds all the grpc requests on the server side and returns the relevant data.
    """

    def CreateEvent(self, request: community_event_pb2.EventDataRequest, context: grpc.ServicerContext) -> community_event_pb2.CreateResponse:
        '''
        This function verifies incoming data and creates a new community event.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("CreateEvent Request Made:")
        print(request)

        success, http_code, message, id = create_event(
            request.user_id,
            request.community_id,
            request.title,
            request.description,
            request.location,
            request.datetime,
            request.duration
            )
        
        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )
        
        return community_event_pb2.CreateResponse(status=status, id=id)


    def ViewOneEvent(self, request: community_event_pb2.ViewOneRequest, context: grpc.ServicerContext) -> community_event_pb2.ViewResponse:
        '''
        This function verifies incoming data and fetches one specified community event.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("ViewOneEvent Request Made:")
        print(request)

        success, http_code, message, event = view_one_event(request.user_id, request.community_id, request.event_id)

        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )
        
        return community_event_pb2.ViewResponse(status=status, event=format_events([event]))


    def ViewEvents(self, request: community_event_pb2.ViewRequest, context: grpc.ServicerContext) -> community_event_pb2.ViewResponse:
        '''
        This function verifies incoming data and fetches community event.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("ViewEvents Request Made:")
        print(request)

        success, http_code, message, event_list = view_community_events(request.user_id, request.community_id, request.offset, request.limit)

        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )
        
        return community_event_pb2.ViewResponse(status=status, events=format_events(event_list))


    def ViewGlobalEvents(self, request: community_event_pb2.ViewGlobalRequest, context: grpc.ServicerContext) -> community_event_pb2.ViewResponse:
        '''
        This function verifies incoming data and fetches global community events.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("ViewGlobalEvents Request Made:")
        print(request)

        success, http_code, message, event_list = view_global_events(request.offset, request.limit)

        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )
        
        return community_event_pb2.ViewResponse(status=status, events=format_events(event_list))


    def EditEvent(self, request: community_event_pb2.EditEventRequest, context: grpc.ServicerContext) -> community_event_pb2.EventResponse:
        '''
        This function verifies incoming data and edits a community event.
        If any errors arise then relevant error messages are returned.
        '''
        
        print("EditEvent Request Made:")
        print(request)

        success, http_code, message, id = edit_event(
            event_id=request.event_id,
            user_id=request.event_data.user_id,
            community_id=request.event_data.community_id,
            title=request.event_data.title,
            description=request.event_data.description,
            location=request.event_data.location,
            datetime=request.event_data.datetime,
            duration=request.event_data.duration
            )

        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )

        return community_event_pb2.EventResponse(status=status, id=id)


    def DeleteEvent(self, request: community_event_pb2.DeleteEventRequest, context: grpc.ServicerContext) -> community_event_pb2.EventResponse:
        '''
        This function verifies incoming data and deletes a community event.
        If any errors arise then relevant error messages are returned.
        '''

        print("DeleteEvent Request Made:")
        print(request)

        success, http_code, message, id = delete_event(event_id=request.event_id, user_id=request.user_id, community_id=request.community_id)

        status = community_event_pb2.EventResponse(
            success=success,
            http_status=http_code,
            error_message=message
        )
        
        return community_event_pb2.EventResponse(status=status, id=id)
