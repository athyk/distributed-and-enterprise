from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Event, EventTag

from backend.community.utils import does_user_have_required_role

from math import inf as INFINITY


def delete_event(event_id: int, user_id: int, community_id: int) -> tuple[bool, int, list]:
    """
    This function verifies incoming data and creates a new community event
    If any errors arise then relevant error messages are returned.
    """

    event_verify, event_error = verify_integer(event_id, 1, INFINITY, 'Event ID')
    user_verify, user_error = verify_integer(user_id, 1, INFINITY, 'User ID')
    community_verify, community_error = verify_integer(community_id, 1, INFINITY, 'Community ID')


    if False in [event_verify, user_verify, community_verify]:

        all_errors = [event_error, user_error, community_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages
    
    with get_db() as session:
        success, message = does_user_have_required_role(session, community_id, user_id, ['moderator', 'admin'])

        if not success:
            return success, 400, message

        event_result = session.query(Event).filter(
            Event.id == event_id,
            Event.community_id == community_id
        ).first()

        if event_result is None:
            return False, 400, ['Event Selected Does Not Exist']

        tag_result = session.query(EventTag).filter(
                Event.id == event_id,
                Event.id == EventTag.event_id
            ).all()

        for tag in tag_result:
            session.delete(tag)

        session.commit()
        session.delete(event_result)
        session.commit()

        return True, 200, []
