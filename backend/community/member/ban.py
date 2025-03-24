from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import CommunityUser, Community

from math import inf as INFINITY


def ban_user(community_id: int, user_id: int, action_user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and bans a user in a community.
    Only Admins can perform these actions
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    action_verify, action_error = verify_integer(action_user_id, 1, INFINITY)
    
    if False in [user_verify, community_verify, action_verify]:

        all_errors = [user_error, community_error, action_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages
    
    with get_db() as session:
        role_result = session.query(CommunityUser.role).filter(
            Community.id == community_id,
            Community.id == CommunityUser.community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not role_result:
            return False, 400, ['User Or Community Does Not Exist']
        
        else:
            if role_result[0] not in ['admin']:
                return False, 400, ['User Does Not Have The Required Permission To Perform Requested Action']
            
        role_result = session.query(CommunityUser).filter(
            Community.id == community_id,
            Community.id == CommunityUser.community_id,
            CommunityUser.user_id == action_user_id
        ).first()

        if not role_result:
            return False, 400, ['User Not Within Community']
        
        if role_result.role == 'banned':
            session.delete(role_result)
            session.commit()

            return True, 200, ['User Unbanned']
        
        else:
            role_result.role = 'banned'
            session.commit()

            return True, 200, ['User Banned']
