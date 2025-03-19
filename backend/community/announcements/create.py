from backend.common.utils import verify_string, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement

from backend.community.utils import does_user_have_required_role

from math import inf as INFINITY
from datetime import datetime


def create_announcement(community_id: int, user_id: int, title: str, description: str, tags: list) -> tuple[bool, list]:
    """
    This function verifies incoming data and creates a new community announcement
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 4, 128)
    description_verify, description_error = verify_string(description, 4, 2048)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    

    if False in [user_verify, community_verify, title_verify, description_verify, tags_verify]:

        all_errors = [user_error, community_error, title_error, description_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages

    with get_db() as session:
        # TODO: Rework to new structure

        return True, []
