from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import CommunityUser, Community

from math import inf as INFINITY


def get_all_community_users(community_id: int, user_id: int, action_user_id: int) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and gets all users in a community.
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    
    if False in [user_verify, community_verify]:

        all_errors = [user_error, community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages
    
    with get_db() as session:
        community_result = session.query(Community.public).filter(Community.id == community_id).first()

        if community_result is None:
            return False, 404, ['Community Does Not Exist']
        
        user_result = session.query(CommunityUser.role).filter(
            CommunityUser.community_id == community_id,
            CommunityUser.user_id == user_id
            ).first()

        if not user_result: # No relation to community and user
            if not community_result[0]: # Community in question is private
                return False, 403, ['User Not Part Of Community'], []
            
            user_result = session.query(CommunityUser).filter(
                CommunityUser.community_id == community_id
            ).all()

            formatted_result = [[user.id, user.name] for user in user_result]

            return True, 200, [], formatted_result
        
        user_result = session.query(CommunityUser).filter(
            CommunityUser.community_id == community_id
        ).all()

        formatted_result = [[user.id, user.name] for user in user_result]

        return True, 200, [], formatted_result
