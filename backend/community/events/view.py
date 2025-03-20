from backend.common.utils import verify_integer
from backend.community.database.database import get_db

from math import inf as INFINITY


def view_one_event(user_id: int, community_id: int, event_id: int) -> tuple[bool, int, list, dict]:
    """
    This function verifies incoming data and fetches a community event
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    event_verify, event_error = verify_integer(event_id, 1, INFINITY)

    if False in [user_verify, community_verify, event_verify]:

        all_errors = [user_error, community_error, event_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, {}

    with get_db() as session:
        return True, 200, [], {}


def view_community_events(user_id: int, community_id: int, offset: int, limit: int) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and fetches a range of community event
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [user_verify, community_verify, offset_verify, limit_verify]:

        all_errors = [user_error, community_error, offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []

    with get_db() as session:
        return True, 200, [], []


def view_global_events(offset: int, limit: int) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and fetches global community events
    If any errors arise then relevant error messages are returned.
    """

    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [offset_verify, limit_verify]:

        all_errors = [offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []

    with get_db() as session:
        return True, 200, [], []
