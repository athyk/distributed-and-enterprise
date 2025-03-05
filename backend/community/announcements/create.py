from backend.common.utils import verify_string, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Announcement

from backend.community.announcements.local_functions import add_tags
from backend.community.utils import does_user_have_required_role

from math import inf as INFINITY
from datetime import datetime


def create_announcement(community_id: int, user_id: int, title: str, description: str, tags: list) -> tuple[bool, list]:
    """
    This function verifies incoming data and creates a new community announcement
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    title_verify, title_error = verify_string(title, 4, 128)
    description_verify, description_error = verify_string(description, 4, 2048)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    

    if False in [user_verify, community_verify, title_verify, description_verify, tags_verify]:

        all_errors = [user_error, community_error, title_error, description_error, tags_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, error_messages

    with get_db() as session:
        success, message = does_user_have_required_role(session, community_id, user_id, ['Moderator', 'Admin'])
        
        if not success:
            return success, message
            
        new_announcement = Announcement(
            community_id=community_id,
            user_id=user_id,
            title=title,
            description=description,
            datetime=datetime.utcnow(),
            edit_datetime=None,
            last_edited_user_id=None
        )

        session.add(new_announcement)
        session.commit()

        new_announcement_id = new_announcement.id
        further_non_critical_errors = ['Community Announcement Successfully Created']

        further_non_critical_errors = add_tags(session, tags, new_announcement_id, further_non_critical_errors)

        return True, further_non_critical_errors
