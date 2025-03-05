from backend.community.database.models import Tag, AnnouncementTag


def add_tags(session: any, tags: list, announcement_id: int, further_non_critical_errors: list) -> list:
    """
    This function searches for the tags provided and connects them to -
    the Announcement in the AnnouncementTag table
    """

    for tag in tags:
        result = session.query(Tag.id).filter(Tag.name == tag).first()

        if not result:
            error = f'Community Announcement Tag ({tag}) Does Not Exist. Tag Not Applied.'
            further_non_critical_errors.append(error)

        else:
            append_tag = AnnouncementTag(
                announcement_id=announcement_id,
                tag_id=result[0]
            )

            session.add(append_tag)

    session.commit()

    return further_non_critical_errors
