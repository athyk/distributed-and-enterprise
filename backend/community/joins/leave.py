from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import CommunityUser

from math import inf as INFINITY

def remove_user_in_community(community_id: int, user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and removes a user from the community.
    If they are banned, the action is interrupted.
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    
    if False in [user_verify, community_verify]:

        all_errors = [user_error, community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages
    
    with get_db() as session:
        user_exists = session.query(CommunityUser).filter(
            CommunityUser.community_id == community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not user_exists:
            return False, 400, ['User Is Not Part Of Community']
        
        if user_exists.role == 'banned':
            return False, 403, ['Unable To Perform Action']
        
        session.delete(user_exists)
        session.commit()

        return True, 200, []
