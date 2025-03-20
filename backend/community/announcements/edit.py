from backend.common.utils import verify_string, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement, AnnouncementTag
from backend.community.announcements.local_functions import add_tags

from backend.community.utils import check_if_user_is_in_private_community, does_user_have_required_role, remove_duplicate_from_two_lists

from math import inf as INFINITY
from datetime import datetime


def edit_announcement(announcement_id: int, community_id: int, user_id: int, title: str, description: str, tags: list) -> tuple[bool, list]:
    """
    This function verifies incoming data and creates a new community announcement
    If any errors arise then relevant error messages are returned.
    """
    announcement_verify, announcement_error = verify_integer(announcement_id, 1, INFINITY)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 4, 128)
    description_verify, description_error = verify_string(description, 4, 2048)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    
    if False in [announcement_verify, user_verify, community_verify, title_verify, description_verify, tags_verify]:
        all_errors = [announcement_error, user_error, community_error, title_error, description_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]
        return False, error_messages
    
    print('passed')
    
    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, message
        
        success, message = does_user_have_required_role(session, community_id, user_id, ['moderator', 'admin'])

        if not success:
            return success, message
        
        print('accepted')

        row = session.query(Announcement).filter_by(
            id=announcement_id,
            community_id=community_id
            ).first()

        if row is None:
            return False, ['Announcement Provided Does Not Exist']
        
        print('got it')

        row.title = title
        row.description = description

        row.last_edited_user_id = int(user_id)
        row.edit_datetime = datetime.utcnow()

        session.commit()

        print('committed')
        
        current_tags = []

        tag_result = session.query(AnnouncementTag.tag_id).filter(
            Announcement.id == announcement_id,
            Announcement.id == AnnouncementTag.announcement_id
        ).all()

        for tag in tag_result:
            current_tags.append(int(tag[0]))

        print(current_tags)
        print(tags)

        current_tags, tags = remove_duplicate_from_two_lists(current_tags, tags)

        print('tagging')
        print(current_tags)
        print(tags)

        for tag in current_tags:
            tag_result = session.query(AnnouncementTag).filter(
                Announcement.id == announcement_id,
                Announcement.id == AnnouncementTag.announcement_id,
                AnnouncementTag.tag_id == tag
            ).first()

            print('got tag')
            print(tag_result)

            session.delete(tag_result)

            print('deleted')

        add_tags(session, tags, announcement_id)

        print('tagged')

        return True, ['Community Announcement Successfully Changed']
