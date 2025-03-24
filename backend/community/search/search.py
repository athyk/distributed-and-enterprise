from backend.common.utils import verify_integer, verify_boolean, verify_string, verify_list
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser, CommunityTag, CommunityDegree
from sqlalchemy import func

from math import inf as INFINITY


def search_for_community(user_id: int, is_with: int, name: str, public: int, minimum_members: int, tags: list, degrees: list) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and invites a user to the community.
    Only Moderators and Admins can perform these actions
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 0, INFINITY)
    with_verify, with_error = verify_integer(is_with, 0, 2)
    name_verify, name_error = verify_string(name, 1, 128)
    public_verify, public_error = verify_integer(public, 0, 2)
    members_verify, members_error = verify_integer(minimum_members, 1, INFINITY)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    degrees_verify, degrees_error = verify_list(degrees, 0, 5)
    
    if False in [user_verify, with_verify, name_verify, public_verify, members_verify, tags_verify, degrees_verify]:

        all_errors = [user_error, with_error, name_error, public_error, members_error, tags_error, degrees_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []
    
    with get_db() as session:
        query = session.query(Community)

        if name:
            query = query.filter(Community.name.startswith(name))

        if public == 1:
            query = query.filter(Community.public.is_(True))
        elif public == 2:
            query = query.filter(Community.public.is_(False))

        if minimum_members > 0:
            query = query.join(CommunityUser).group_by(Community.id).having(func.count(CommunityUser.community_id) > minimum_members)

        if len(tags) > 0:
            for tag_id in tags:
                query = query.filter(Community.id == CommunityTag.community_id, CommunityTag.tag_id == tag_id)

        if len(degrees) > 0:
            for degree_id in degrees:
                query = query.filter(Community.id == CommunityDegree.community_id, CommunityDegree.degree_id == degree_id)

        if user_id > 0:
            if is_with == 1:
                query = query.filter(Community.id == CommunityUser.community_id, CommunityUser.user_id == user_id)
            elif is_with == 2:
                query = query.filter(Community.id == CommunityUser.community_id, CommunityUser.user_id != user_id)

        try:
            results = query.all()

            return True, 200, [], results

        except Exception:
            return False, 500, ['Internal Server Error', 'Community Searching Abandoned'], []
