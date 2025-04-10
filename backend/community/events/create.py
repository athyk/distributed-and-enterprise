from backend.common.utils import verify_string, verify_integer, verify_list
from backend.community.database.database import get_db
from backend.community.database.models import Event

from backend.community.utils import does_user_have_required_role
from backend.community.events.local_functions import location_name_to_coords, add_tags

from math import inf as INFINITY


def create_event(user_id: int, community_id: int, title: str, description: str, location: str, datetime: str, duration: int, tags: list,lat_lng: list[float] = None) -> tuple[bool, int, list, int]:
    """
    This function verifies incoming data and creates a new community event
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    title_verify, title_error = verify_string(title, 1, 50, 'Title')
    description_verify, description_error = verify_string(description, 1, 1024, 'Description')
    location_verify, location_error = verify_string(location, 1, 2048, 'Location') if location else (True, 'None')
    datetime_verify, datetime_error = verify_string(datetime, 10, 10, 'DateTime')
    duration_verify, duration_error = verify_integer(duration, 1, 672, 'Duration')
    tags_verify, tags_error = verify_list(tags, 0, 5, 'Tags')
    lat_lng_verify, lat_lng_error = verify_list(lat_lng, 2, 2, 'Latitude and Longitude') if lat_lng else (True, '')

    if False in [user_verify, community_verify, title_verify, description_verify, location_verify, datetime_verify, duration_verify, tags_verify,lat_lng_verify]:

        all_errors = [user_error, community_error, title_error, description_error, location_error, datetime_error, duration_error, tags_error,lat_lng_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, -1
    
    with get_db() as session:
        success, message = does_user_have_required_role(session, community_id, user_id, ['moderator', 'admin'])

        if not success:
            return success, 403, message, -1

        new_event = Event(
            community_id=community_id,
            title=title,
            description=description,
            location=location,
            datetime=datetime,
            duration=duration
        )

        print(f"lat_lng: {lat_lng}")
        if lat_lng and len(lat_lng) == 2:
            lng, lat = lat_lng
        else:
            success, lng, lat, message = location_name_to_coords(location)

        if success:
            new_event.longitude = lng
            new_event.latitude = lat

        session.add(new_event)
        session.commit()

        new_event_id = new_event.id
        
        add_tags(session, tags, new_event_id)

        return True, 200, message, new_event_id
