from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag, Community
from backend.community.utils import check_if_user_is_in_private_community

from math import inf as INFINITY


def get_community_announcements(community_id: int, user_id: int, offset: int, limit: int) -> tuple[bool, list, list]:
    """
    This function verifies incoming data and returns the specified community data
    If any errors arise then relevant error messages are returned.
    """

    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [community_verify, user_verify, offset_verify, limit_verify]:

        all_errors = [community_error, user_error, offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, []

    with get_db() as session:
        # TODO: Rework to new structure

        return True, ['Announcements Fetched'], []


def get_specified_community_announcement(announcement_id: int, community_id: int, user_id: int) -> tuple[bool, list, dict]:
    """
    This function verifies incoming data and returns the specified community data
    If any errors arise then relevant error messages are returned.
    """

    announcement_verify, announcement_error = verify_integer(announcement_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)

    if False in [community_verify, user_verify, announcement_verify]:

        all_errors = [community_error, user_error, announcement_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, {}

    with get_db() as session:
        # TODO: Rework to new structure

        return True, ['Announcement Fetched'], {}


def get_global_community_announcements(offset: int, limit: int) -> tuple[bool, list, list]:
    """
    This function verifies incoming data and returns the specified announcements
    If any errors arise then relevant error messages are returned.
    """

    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [offset_verify, limit_verify]:

        all_errors = [offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, []

    with get_db() as session:
        # TODO: Rework to new structure

        return True, ['Announcements Fetched'], []
