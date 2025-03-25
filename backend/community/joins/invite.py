from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser
from backend.community.joins.join import update_user

from math import inf as INFINITY


def invite_user_to_community(community_id: int, user_id: int, invite_user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and invites a user to the community.
    Only Moderators and Admins can perform these actions
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    invite_verify, invite_error = verify_integer(invite_user_id, 1, INFINITY, 'Invite User ID')
    
    if False in [user_verify, community_verify, invite_verify]:

        all_errors = [user_error, community_error, invite_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    
    with get_db() as session:
        role_result = session.query(CommunityUser.role).filter(
            Community.id == community_id,
            Community.id == CommunityUser.community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not role_result:
            return False, ['User Or Community Does Not Exist']
        
        else:
            if role_result[0] not in ['moderator', 'admin']:
                return False, ['User Does Not Have The Required Permission To Perform Requested Action']
            
        user_exists = session.query(CommunityUser.role).filter(
            CommunityUser.community_id == community_id,
            CommunityUser.user_id == invite_user_id
        ).first()

        if user_exists:
            if user_exists[0] == 'invited':
                return False, 400, ['User Has Already Been Sent An Invite']
            
            elif user_exists[0] == 'banned':
                return False, 403, ['User Is Banned', 'Invite Not Created']
            
            elif user_exists[0] == 'requested':
                return update_user(session, community_id, invite_user_id, ['User Requested To Join', 'User Has Joined Community'])

            return False, 400, ['User Is Already With Community']
        
        invite = CommunityUser(
            community_id=community_id,
            user_id=invite_user_id,
            role='invited'
        )

        session.add(invite)
        session.commit()

        return True, 200, []
