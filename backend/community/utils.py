from backend.community.database.models import Community, CommunityUser
from backend.common.services import TagsClient, DegreesClient
from backend.common.proto import tag_pb2, degree_pb2


def check_if_user_is_in_private_community(session: any, community_id: int, user_id: int) -> tuple[bool, list]:
    """
    This function checks whether the user is in a community that is private
    If the community is public then access is granted for further functionality.
    If any errors arise then relevant error messages are returned.
    """

    community_result = session.query(Community.public).filter(Community.id == community_id).first()

    if not community_result:
        return False, ['Community Does Not Exist']
        
    if community_result[0] is False:
        user_result = session.query(CommunityUser.role).filter(
            Community.id == community_id,
            Community.id == CommunityUser.community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not user_result:
            return False, ['User Not Part Of Community']
        
        if user_result[0] in ['requested', 'invited', 'banned']:
            return False, ['User Not Part Of Community']

    return True, []


def does_user_have_required_role(session: any, community_id: int, user_id: int, check_roles: list) -> tuple[bool, list]:
    """
    This function checks whether the user has any of the provided roles.
    If any errors arise then relevant error messages are returned.
    """

    role_result = session.query(CommunityUser.role).filter(
        Community.id == community_id,
        Community.id == CommunityUser.community_id,
        CommunityUser.user_id == user_id
        ).first()
    
    if not role_result:
        return False, ['User Not Part Of Community']
    
    if role_result[0] not in check_roles:
        return False, ['User Does Not Have Required Community Role']
    
    return True, []


def remove_duplicate_from_two_lists(list1, list2):
    """
    This function takes in two lists and removes the elements that occur in both from both lists.

    However, if 7 appears once in list1 and then twice in list2 then 7 will only be removed from -
    both lists once, thus leaving a 7 in list2
    """

    final_list1 = list1
    final_list2 = list2

    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                final_list1.remove(item1)
                final_list2.remove(item2)

                return remove_duplicate_from_two_lists(final_list1, final_list2)

    return final_list1, final_list2


def get_tag_name(tag_id):
    """
    Get a specific tag name
    """
    client = TagsClient()

    try:
        req = tag_pb2.TagGetRequest(
            id=tag_id,
        )

        res: tag_pb2.TagGetResponse = client.get(req)

        data = client.tag_to_json(res.tag)

        return data['name']

    except Exception:
        return ''


def get_degree_name(degree_id):
    """
    Get a specific degree name
    """
    client = DegreesClient()

    try:
        req = degree_pb2.DegreeGetRequest(
            id=degree_id,
        )

        res: degree_pb2.DegreeGetResponse = client.get(req)

        data = client.degree_to_json(res.degree)

        return data['name']

    except Exception:
        return ''
