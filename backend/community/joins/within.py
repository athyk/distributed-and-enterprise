from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser

from math import inf as INFINITY

def is_user_in_community(community_id: int, user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and returns the role/state the user is in the community.
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    
    if False in [user_verify, community_verify]:

        all_errors = [user_error, community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    
    with get_db() as session:
        user_exists = session.query(CommunityUser.role).filter(
            CommunityUser.community_id == community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not user_exists:
            return False, 400, ['User Is Not With Community']
        
        return True, 200, [f'User Role: {user_exists[0].upper()}']
