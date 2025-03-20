from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser

from math import inf as INFINITY

def add_user_to_community(community_id: int, user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and adds a user to the community.
    If the community is private, they will request access.
    If the private community has already invited the user, they are added.
    If they are banned, they can not join the community.
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    
    if False in [user_verify, community_verify]:

        all_errors = [user_error, community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    