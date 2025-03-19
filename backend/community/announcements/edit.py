from backend.common.utils import verify_string, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag

from backend.community.utils import check_if_user_is_in_private_community, does_user_have_required_role, remove_duplicate_from_two_lists

from math import inf as INFINITY
from datetime import datetime


def edit_announcement(announcement_id: int, community_id: int, user_id: int, title: str, description: str, tags: list) -> tuple[bool, list]:
    """
    This function verifies incoming data and creates a new community announcement
    If any errors arise then relevant error messages are returned.
    """

    announcement_verify, announcement_error = verify_integer(announcement_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 4, 128)
    description_verify, description_error = verify_string(description, 4, 2048)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    

    if False in [announcement_verify, user_verify, community_verify, title_verify, description_verify, tags_verify]:

        all_errors = [announcement_error, user_error, community_error, title_error, description_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    
    with get_db() as session:
        # TODO: Rework to new structure

        return True, []
