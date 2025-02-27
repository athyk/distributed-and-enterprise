from backend.community.database.models import Tag, Degree, CommunityDegree, CommunityTag


def add_tags(session, tags, community_id, further_non_critical_errors):
    '''
    This function searches for the tags provided and connects them to -
    the Community in the CommunityTag table
    '''

    for tag in tags:
        result = session.query(Tag.id).filter(Tag.name == tag).first()

        if not result:
            error = f'Community Tag ({tag}) Does Not Exist. Tag Not Applied.'
            further_non_critical_errors.append(error)

        else:
            append_tag = CommunityTag(
                community_id=community_id,
                tag_id=result[0]
            )

            session.add(append_tag)
    
    return further_non_critical_errors


def add_degrees(session, degrees, community_id, further_non_critical_errors):
    '''
    This function searches for the degrees provided and connects them to -
    the Community in the CommunityDegree table
    '''

    for degree in degrees:
        result = session.query(Degree.id).filter(Degree.name == degree).first()

        if not result:
            error = f'Degree ({degree}) Does Not Exist. Degree Not Applied.'
            further_non_critical_errors.append(error)

        else:
            append_degree = CommunityDegree(
                community_id=community_id,
                degree_id=result[0]
            )

            session.add(append_degree)

    return further_non_critical_errors
