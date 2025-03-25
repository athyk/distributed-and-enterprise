from backend.common.utils import verify_string, verify_integer, verify_list
from backend.community.database.database import get_db
from backend.community.database.models import Event, EventTag
from backend.community.utils import does_user_have_required_role, remove_duplicate_from_two_lists
from backend.community.events.local_functions import location_name_to_coords, add_tags

from math import inf as INFINITY


def edit_event(event_id: int, user_id: int, community_id: int, title: str, description: str, location: str, datetime: str, duration: int, tags: list) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and creates a new community event
    If any errors arise then relevant error messages are returned.
    """

    event_verify, event_error = verify_integer(event_id, 1, INFINITY, 'Event ID')
    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    title_verify, title_error = verify_string(title, 1, 50, 'Title')
    description_verify, description_error = verify_string(description, 1, 1024, 'Description')
    location_verify, location_error = verify_string(location, 1, 2048, 'Location')
    datetime_verify, datetime_error = verify_string(datetime, 10, 10, 'DateTime')
    duration_verify, duration_error = verify_integer(duration, 1, 672, 'Duration')
    tags_verify, tags_error = verify_list(tags, 0, 5, 'Tags')

    if False in [event_verify, user_verify, community_verify, title_verify, description_verify, location_verify, datetime_verify, duration_verify, tags_verify]:

        all_errors = [event_error, user_error, community_error, title_error, description_error, location_error, datetime_error, duration_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages
    
    with get_db() as session:
        success, message = does_user_have_required_role(session, community_id, user_id, ['moderator', 'admin'])

        if not success:
            return success, 403, message
        
        event = session.query(Event).filter(
            Event.id == event_id,
            Event.community_id == community_id
        ).first()

        if event is None:
            return False, 400, ['Event Does Not Exist']

        previous_location = event.location
        
        event.title=title
        event.description=description
        event.location=location
        event.datetime=datetime
        event.duration=duration

        if previous_location != location:
            success, lng, lat, message = location_name_to_coords(location)

            if success:
                event.longitude = lng
                event.latitude = lat

        session.commit()

        current_tags = []

        tag_result = session.query(EventTag.tag_id).filter(
            Event.id == event_id,
            Event.id == EventTag.event_id
        ).all()

        for tag in tag_result:
            current_tags.append(int(tag[0]))

        current_tags, tags = remove_duplicate_from_two_lists(current_tags, tags)

        for tag in current_tags:
            tag_result = session.query(EventTag).filter(
                Event.id == event_id,
                Event.id == EventTag.event_id,
                EventTag.tag_id == tag
            ).first()

            session.delete(tag_result)

        add_tags(session, tags, event_id)

        return True, 200, message
