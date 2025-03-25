from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser

from math import inf as INFINITY

def insert_user(session: any, community_id: int, user_id: int, role: str = 'user') -> tuple[bool, int, list]:
    try:
        new_user = CommunityUser(
            community_id=community_id,
            user_id=user_id,
            role=role
        )

        session.add(new_user)
        session.commit()

        return True, 201, []

    except Exception:
        session.rollback()

        return False, 500, ['Internal Server Error', 'Unable To Join Community']


def update_user(session: any, community_id: int, user_id: int, success_message: list=[]) -> tuple[bool, int, list]:
    try:
        update_user = session.query(CommunityUser).filter(
            CommunityUser.community_id==community_id,
            CommunityUser.user_id==user_id
            ).first()
        
        if update_user:
            update_user.role = 'user'
            session.commit()

            print('converted to user')

            return True, 201, success_message

        else:
            return False, 400, ['User Not Invited']

    except Exception:
        session.rollback()

        return False, 500, ['Internal Server Error', 'Unable To Join Community']


def add_user_to_community(community_id: int, user_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and adds a user to the community.
    If the community is private, they will request access.
    If the private community has already invited the user, they are added.
    If they are banned, they can not join the community.
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
                return insert_user(session, community_id, user_id, 'requested')

            else: # Add user to public server
                return insert_user(session, community_id, user_id)

        else: # Some Trace Of The User In The Community
            if user_result[0] == 'banned':
                return False, 403, ['User Is Banned From The Community']
            
            elif user_result[0] == 'invited':
                return update_user(session, community_id, user_id)
            
            elif user_result[0] == 'requested':
                return False, 400, ['User Has Requested Access To The Community']
            
            else:
                return False, 400, ['User Is Already With The Community']
