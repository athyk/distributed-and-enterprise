from backend.common.utils import verify_string, verify_integer, verify_list
from backend.community.database.database import get_db

from backend.community.utils import does_user_have_required_role

from math import inf as INFINITY


def edit_event(event_id: int, user_id: int, community_id: int, title: str, description: str, location: str, datetime: str, duration: int, tags: list) -> tuple[bool, int, list, int]:
    """
    This function verifies incoming data and creates a new community event
    If any errors arise then relevant error messages are returned.
    """

    event_verify, event_error = verify_integer(event_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 1, 50)
    description_verify, description_error = verify_string(description, 1, 1024)
    location_verify, location_error = verify_string(location, 1, 2048)
    datetime_verify, datetime_error = verify_string(datetime, 10, 10)
    duration_verify, duration_error = verify_integer(duration, 1, 672)
    tags_verify, tags_error = verify_list(tags, 0, 5)

    if False in [event_verify, user_verify, community_verify, title_verify, description_verify, location_verify, datetime_verify, duration_verify, tags_verify]:

        all_errors = [event_error, user_error, community_error, title_error, description_error, location_error, datetime_error, duration_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, -1
    
    with get_db() as session:
        success, message = does_user_have_required_role(session, community_id, user_id, ['moderator', 'admin'])

        if not success:
            return success, 403, message, -1



        return True, 200, [], -1
