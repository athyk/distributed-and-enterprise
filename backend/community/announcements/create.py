from backend.common.utils import verify_string, verify_boolean, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser, Announcement

from backend.community.crud.local_functions import add_tags, add_degrees

from math import inf as INFINITY


def create_community(community_id: int, user_id: int, title: str, description: str, tags: list) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and creates a new community announcement
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 4, 64)
    description_verify, description_error = verify_string(description, 4, 2048)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    

    if False in [user_verify, community_verify, title_verify, description_verify, tags_verify]:

        all_errors = [user_error, community_error, title_error, description_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages

    with get_db() as session:
        pass


