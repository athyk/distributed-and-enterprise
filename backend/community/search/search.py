from backend.common.utils import verify_integer, verify_string, verify_list
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser, CommunityTag, CommunityDegree
from backend.community.utils import get_tag_name, get_degree_name
from sqlalchemy import func, exists

from math import inf as INFINITY


def search_for_community(offset: int, limit: int, user_id: int, is_with: int, name: str, public: int, minimum_members: int, tags: list, degrees: list) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and filters communities.
    Only Moderators and Admins can perform these actions
    If any errors arise then relevant error messages are returned.
    """

    offset_verify, offset_error = verify_integer(offset, 0, INFINITY, 'Offset')
    limit_verify, limit_error = verify_integer(limit, 1, 50, 'Limit')
    user_verify, user_error = verify_integer(user_id, 0, INFINITY, 'User ID')
    with_verify, with_error = verify_integer(is_with, 0, 2, 'Is With')
    name_verify, name_error = verify_string(name, 0, 128, 'Name')
    public_verify, public_error = verify_integer(public, 0, 2, 'Public')
    members_verify, members_error = verify_integer(minimum_members, 0, INFINITY, 'Minimum Members')
    tags_verify, tags_error = verify_list(tags, 0, 5, 'Tags')
    degrees_verify, degrees_error = verify_list(degrees, 0, 5, 'Degrees')

    if False in [offset_verify, limit_verify, user_verify, with_verify, name_verify, public_verify, members_verify, tags_verify, degrees_verify]:

        all_errors = [offset_error, limit_error, user_error, with_error, name_error, public_error, members_error, tags_error, degrees_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []

    with get_db() as session:
        query = session.query(Community.id, Community.name, Community.description, Community.public)

        if name != '':
            query = query.filter(Community.name.startswith(name))

        if public == 1:
            query = query.filter(Community.public.is_(True))
        elif public == 2:
            query = query.filter(Community.public.is_(False))

        if minimum_members > 0:
            query = query.join(CommunityUser).group_by(Community.id).having(func.count(CommunityUser.community_id) > minimum_members)

        if len(tags) > 0:
            for tag_id in tags:
                query = query.join(CommunityTag).filter(CommunityTag.tag_id == tag_id)

        if len(degrees) > 0:
            for degree_id in degrees:
                query = query.join(CommunityDegree).filter(CommunityDegree.degree_id == degree_id)

        if user_id > 0:
            if is_with == 1:
                query = query.filter(Community.id == CommunityUser.community_id, CommunityUser.user_id == user_id)
            elif is_with == 2:
                query = query.filter(~exists().where((CommunityUser.community_id == Community.id) & (CommunityUser.user_id == user_id)))

        results = query.order_by(Community.id.asc()).offset(offset).limit(limit).all()

        communities = []

        for community in results:
            community_tag_result = session.query(CommunityTag.tag_id).filter(
                Community.id == community[0],
                Community.id == CommunityTag.community_id
            ).all()

            tags = []

            for tag in community_tag_result:
                tags.append(get_tag_name(tag[0]))

            community_degree_result = session.query(CommunityDegree.degree_id).filter(
                Community.id == community[0],
                Community.id == CommunityDegree.community_id
            ).all()

            degrees = []

            for degree in community_degree_result:
                degrees.append(get_degree_name(degree[0]))

            member_count = session.query(func.count(CommunityUser.community_id)).filter(CommunityUser.community_id == community[0]).first()

            reformed_community = {
                "id": community[0],
                "name": community[1],
                "description": community[2],
                "public": int(community[3]),
                "tags": tags,
                "degrees": degrees,
                "member_count": member_count[0]
            }

            communities.append(reformed_community)

        return True, 200, [], communities
