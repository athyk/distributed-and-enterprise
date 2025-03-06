from backend.auth.database.models import Tag, UserTag


def add_tags(session, tags, user_id, further_non_critical_errors):
    """
    This function searches for the tags provided and connects them to -
    the User in the UserTag table
    """

    for tag in tags:
        result = session.query(Tag.id).filter(Tag.name == tag).first()

        if not result:
            error = f'User Tag ({tag}) Does Not Exist. Tag Not Applied.'
            further_non_critical_errors.append(error)

        else:
            append_tag = UserTag(
                user_id=user_id,
                tag_id=result[0]
            )

            session.add(append_tag)
    
    return further_non_critical_errors
