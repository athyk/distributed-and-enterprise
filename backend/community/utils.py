from backend.community.database.models import Community, CommunityUser


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
        user_result = session.query(CommunityUser.user_id).filter(
            Community.id == community_id,
            Community.id == CommunityUser.community_id,
            CommunityUser.user_id == user_id
        ).first()

        if not user_result:
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
