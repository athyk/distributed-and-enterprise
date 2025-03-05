from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag, Tag
from backend.community.utils import check_if_user_is_in_private_community

from math import inf as INFINITY


def get_community_announcements(community_id: int, user_id: int, offset: int, limit: int) -> tuple[bool, list, list]:
    """
    This function verifies incoming data and returns the specified community data
    If any errors arise then relevant error messages are returned.
    """

    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [community_verify, user_verify, offset_verify, limit_verify]:

        all_errors = [community_error, user_error, offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, []

    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, message, []
            
        announcement_result = session.query(
            Announcement.id, Announcement.title, Announcement.description, Announcement.user_id,
            Announcement.datetime, Announcement.last_edited_user_id, Announcement.edit_datetime
        ).filter(
            Announcement.community_id == community_id
        ).order_by(
            Announcement.datetime.desc()
        ).limit(limit).offset(offset).all()

        announcement_result = [list(_tuple) for _tuple in announcement_result]

        announce = []

        for announcement in announcement_result:
            announcement_id = announcement[0]

            announcement_tag_result = session.query(Tag.name).filter(
                Announcement.id == announcement_id,
                Announcement.id == AnnouncementTag.announcement_id,
                AnnouncementTag.tag_id == Tag.id
            ).all()

            tags = []

            for tag in announcement_tag_result:
                tags.append(tag)

            reformed_announcement = {
                "id": announcement[0],
                "title": announcement[1],
                "description": announcement[2],
                "tags": tags,
                "user_id": announcement[3],
                "uploaded": announcement[4].strftime("%Y-%m-%d %H:%M:%S"),
                "edit_user_id": announcement[5],
                "edit_uploaded": announcement[6].strftime("%Y-%m-%d %H:%M:%S")
            }

            announce.append(reformed_announcement)

        return True, ['Announcements Fetched'], announce
