from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag

from backend.community.utils import check_if_user_is_in_private_community, does_user_have_required_role

from math import inf as INFINITY


def delete_announcement(announcement_id: int, community_id: int, user_id: int) -> tuple[bool, list]:
    """
    This function verifies incoming data and deletes the specified community announcement
    If any errors arise then relevant error messages are returned.
    """

    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)

    if False in [community_verify, user_verify]:

        all_errors = [community_error, user_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    
    with get_db() as session:
        # TODO: Rework to new structure

        return True, ['Announcement Successfully Deleted']
        
