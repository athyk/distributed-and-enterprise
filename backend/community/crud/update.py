from backend.common.utils import verify_string, verify_boolean, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityDegree, CommunityTag, CommunityUser

from backend.community.crud.local_functions import add_tags, add_degrees
from backend.community.utils import remove_duplicate_from_two_lists

from math import inf as INFINITY

def update_community(community_id: int, name: str, description: str, public: bool, tags: list, degrees: list, user_id: int) -> tuple[bool, list]:
    """
    This function verifies incoming data and updates the specified community
    If any errors arise then relevant error messages are returned.
    """

    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    name_verify, name_error = verify_string(name, 4, 64)
    description_verify, description_error = verify_string(description, 4, 511)
    public_verify, public_error = verify_boolean(public)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    degrees_verify, degrees_error = verify_list(degrees, 0, 5)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)

    if False in [community_verify, name_verify, description_verify, public_verify, tags_verify, degrees_verify, user_verify]:

        all_errors = [community_error, name_error, description_error, public_error, tags_error, degrees_error, user_error]
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
            if role_result[0] != 'Admin':
                return False, ['User Does Not Have The Required Permission To Perform Requested Action']

        try:
            row = session.query(Community).filter_by(id=community_id).first()

            row.name = name
            row.description = description
            row.public = public

            session.commit()

        except Exception as e:
            print(e)
            return False, ['Community Does Not Exist']

        current_tags = []
        current_degrees = []

        tag_result = session.query(CommunityTag.tag_id).filter(
            CommunityTag.community_id == community_id
        ).all()

        for tag in tag_result:
            current_tags.append(str(tag[0]))
        
        degree_result = session.query(CommunityDegree.degree_id).filter(
            CommunityDegree.community_id == community_id
        ).all()

        for degree in degree_result:
            current_degrees.append(degree[0])

        current_tags, tags = remove_duplicate_from_two_lists(current_tags, tags)
        current_degrees, degrees = remove_duplicate_from_two_lists(current_degrees, degrees)

        for tag in current_tags:
            tag_result = session.query(CommunityTag).filter(
                CommunityTag.community_id == community_id,
                CommunityTag.tag_id == tag
            ).first()

            session.delete(tag_result)

        for degree in current_degrees:
            degree_result = session.query(CommunityDegree).filter(
                Community.id == CommunityDegree.community_id,
                CommunityDegree.degree_id == degree
            ).first()

            session.delete(degree_result)

        further_non_critical_errors = ['Community Successfully Updated']

        further_non_critical_errors = add_tags(session, tags, community_id, further_non_critical_errors)
        further_non_critical_errors = add_degrees(session, degrees, community_id, further_non_critical_errors)

        session.commit()

        return True, further_non_critical_errors
