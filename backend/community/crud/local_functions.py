from backend.community.database.models import CommunityDegree, CommunityTag


def add_tags(session, tags, community_id, further_non_critical_errors):
    """
    This function searches for the tags provided and connects them to -
    the Community in the CommunityTag table
    """

    for tag in tags:
        append_tag = CommunityTag(
            community_id=community_id,
            tag_id=tag
        )

        session.add(append_tag)
    
    return further_non_critical_errors


def add_degrees(session, degrees, community_id, further_non_critical_errors):
    """
    This function searches for the degrees provided and connects them to -
    the Community in the CommunityDegree table
    """

    for degree in degrees:
        append_degree = CommunityDegree(
            community_id=community_id,
            degree_id=degree
        )

        session.add(append_degree)

    return further_non_critical_errors
