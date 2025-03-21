from backend.community.database.models import AnnouncementTag
from backend.common.services import TagsClient
from backend.common.proto import tag_pb2


def add_tags(session, tags, announcement_id):
    """
    This function searches for the tags provided and connects them to -
    the Announcement in the AnnouncementTag table
    """

    tag_client = TagsClient()

    for tag in tags:
        res = tag_client.create(tag_pb2.TagCreateRequest(id=tag))

        if res.success:  # Never assume the tag was created, do not error out either
            user_tag = AnnouncementTag(announcement_id=announcement_id, tag_id=tag)
            session.add(user_tag)

    session.commit()
