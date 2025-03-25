from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser, CommunityTag, CommunityDegree
from backend.community.utils import check_if_user_is_in_private_community, does_user_have_required_role

from math import inf as INFINITY


def delete_community(community_id: int, user_id: int) -> tuple[bool, list]:
    """
    This function verifies incoming data and deletes the specified community
    If any errors arise then relevant error messages are returned.
    """

    print(f'deletion user_id: {user_id}')

    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')
    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')

    if False in [community_verify, user_verify]:

        all_errors = [community_error, user_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages
    
    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, message
        
        success, message = does_user_have_required_role(session, community_id, user_id, ['Admin'])
        
        if not success:
            return success, message

        tag_result = session.query(CommunityTag).filter(
                Community.id == community_id,
                Community.id == CommunityTag.community_id
            ).all()
        
        for tag in tag_result:
            session.delete(tag)

        degree_result = session.query(CommunityDegree).filter(
                Community.id == community_id,
                Community.id == CommunityDegree.community_id
            ).all()
        
        for degree in degree_result:
            session.delete(degree)

        user_result = session.query(CommunityUser).filter(
                Community.id == community_id,
                Community.id == CommunityUser.community_id
            ).all()
        
        for user in user_result:
            session.delete(user)

        session.commit()

        result = session.query(Community).filter(Community.id == community_id).first()
        session.delete(result)

        session.commit()

        return True, ['Community Successfully Deleted']
