from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag, Community
from backend.community.utils import check_if_user_is_in_private_community, get_tag_name

from math import inf as INFINITY


def get_community_announcements(community_id: int, user_id: int, offset: int, limit: int) -> tuple[bool, list, list]:
    """
    This function verifies incoming data and returns the specified community announcement data
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

            announcement_tag_result = session.query(AnnouncementTag.tag_id).filter(
                Announcement.id == announcement_id,
                Announcement.id == AnnouncementTag.announcement_id
            ).all()

            tags = []

            for tag in announcement_tag_result:
                tags.append(get_tag_name(tag[0]))

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


def get_specified_community_announcement(announcement_id: int, community_id: int, user_id: int) -> tuple[bool, list, dict]:
    """
    This function verifies incoming data and returns the specified community data
    If any errors arise then relevant error messages are returned.
    """

    announcement_verify, announcement_error = verify_integer(announcement_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)

    if False in [community_verify, user_verify, announcement_verify]:

        all_errors = [community_error, user_error, announcement_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, {}

    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, message, {}

        announcement_result = session.query(
            Announcement.id, Announcement.title, Announcement.description, Announcement.user_id,
            Announcement.datetime, Announcement.last_edited_user_id, Announcement.edit_datetime
        ).filter(
            Announcement.id == announcement_id
        ).first()

        if announcement_result is None:
            return False, ['Specified Announcement Does Not Exist Within Community'], {}

        announcement_tag_result = session.query(AnnouncementTag.tag_id).filter(
            Announcement.id == announcement_id,
            Announcement.id == AnnouncementTag.announcement_id
        ).all()

        tags = []

        for tag in announcement_tag_result:
            tags.append(get_tag_name(tag[0]))

        reformed_announcement = {
            "id": announcement_result[0],
            "title": announcement_result[1],
            "description": announcement_result[2],
            "tags": tags,
            "user_id": announcement_result[3],
            "uploaded": announcement_result[4].strftime("%Y-%m-%d %H:%M:%S"),
            "edit_user_id": announcement_result[5],
            "edit_uploaded": announcement_result[6].strftime("%Y-%m-%d %H:%M:%S")
        }

        return True, ['Announcement Fetched'], reformed_announcement


def get_global_community_announcements(offset: int, limit: int) -> tuple[bool, list, list]:
    """
    This function verifies incoming data and returns the specified announcements
    If any errors arise then relevant error messages are returned.
    """

    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [offset_verify, limit_verify]:

        all_errors = [offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages, []

    with get_db() as session:
        announcement_result = session.query(
            Announcement.id, Announcement.title, Announcement.description, Announcement.user_id,
            Announcement.datetime, Announcement.last_edited_user_id, Announcement.edit_datetime, Announcement.community_id
        ).filter(
            Announcement.community_id == Community.id,
            Community.public
        ).order_by(
            Announcement.datetime.desc(),
            Announcement.id.asc()
        ).limit(limit).offset(offset).all()

        announcement_result = [list(_tuple) for _tuple in announcement_result]

        announce = []

        for announcement in announcement_result:
            announcement_tag_result = session.query(AnnouncementTag.tag_id).filter(
                Announcement.id == announcement[0],
                Announcement.id == AnnouncementTag.announcement_id
            ).all()

            tags = []

            for tag in announcement_tag_result:
                tags.append(get_tag_name(tag[0]))

            if announcement[6] is not None:
                announcement[6].strftime("%Y-%m-%d %H:%M:%S")
            else:
                announcement[6] = ''

            if announcement[5] is None:
                announcement[5] = 0

            reformed_announcement = {
                "id": announcement[0],
                "title": announcement[1],
                "description": announcement[2],
                "tags": tags,
                "user_id": announcement[3],
                "uploaded": announcement[4].strftime("%Y-%m-%d %H:%M:%S"),
                "edit_user_id": announcement[5],
                "edit_uploaded": announcement[6],
                "community_id": announcement[7]
            }

            announce.append(reformed_announcement)

        return True, ['Announcements Fetched'], announce
