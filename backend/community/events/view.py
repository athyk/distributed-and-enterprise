from backend.common.utils import verify_integer
from backend.community.database.database import get_db
from backend.community.utils import check_if_user_is_in_private_community, get_tag_name
from backend.community.database.models import Event, EventTag, Community

from math import inf as INFINITY


def view_one_event(user_id: int, community_id: int, event_id: int) -> tuple[bool, int, list, dict]:
    """
    This function verifies incoming data and fetches a community event
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    event_verify, event_error = verify_integer(event_id, 1, INFINITY)

    if False in [user_verify, community_verify, event_verify]:

        all_errors = [user_error, community_error, event_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, {}

    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, 403, message, {}

        event_result = session.query(
            Event.id, Event.community_id, Event.title, Event.description,
            Event.location, Event.latitude, Event.longitude, Event.datetime, Event.duration
        ).filter(
            Event.id == event_id
        ).first()

        if event_result is None:
            return False, 400, ['Specified Event Does Not Exist Within Community'], {}

        event_tag_result = session.query(EventTag.tag_id).filter(
            Event.id == event_id,
            Event.id == EventTag.event_id
        ).all()

        tags = []

        for tag in event_tag_result:
            tags.append(get_tag_name(tag[0]))

        reformed_event = {
                'id': event_id,
                'community_id': event_result[1],
                'title': event_result[2],
                'description': event_result[3],
                'location': event_result[4],
                'latitude': event_result[5],
                'longitude': event_result[6],
                'datetime': event_result[7].strftime("%Y-%m-%d %H:%M:%S"),
                'duration': event_result[8],
                'tags': tags
            }

        return True, 200, ['Event Fetched'], reformed_event


def view_community_events(user_id: int, community_id: int, offset: int, limit: int) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and fetches a range of community event
    If any errors arise then relevant error messages are returned.
    """

    user_verify, user_error = verify_integer(user_id, 1, INFINITY)
    community_verify, community_error = verify_integer(community_id, 1, INFINITY)
    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [user_verify, community_verify, offset_verify, limit_verify]:

        all_errors = [user_error, community_error, offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []

    with get_db() as session:
        success, message = check_if_user_is_in_private_community(session, community_id, user_id)

        if not success:
            return success, 403, message, []

        event_result = session.query(
            Event.id, Event.community_id, Event.title, Event.description,
            Event.location, Event.latitude, Event.longitude, Event.datetime, Event.duration
        ).filter(
            Event.community_id == community_id
        ).order_by(
            Event.datetime.desc(),
            Event.id.asc()
        ).limit(limit).offset(offset).all()

        event_result = [list(_tuple) for _tuple in event_result]

        eve = []

        for event in event_result:
            event_id = event[0]

            event_tag_result = session.query(EventTag.tag_id).filter(
                Event.id == event_id,
                Event.id == EventTag.event_id
            ).all()

            tags = []

            for tag in event_tag_result:
                tags.append(get_tag_name(tag[0]))

            reformed_event = {
                'id': event_id,
                'community_id': event[1],
                'title': event[2],
                'description': event[3],
                'location': event[4],
                'latitude': event[5],
                'longitude': event[6],
                'datetime': event[7].strftime("%Y-%m-%d %H:%M:%S"),
                'duration': event[8],
                'tags': tags
            }

            eve.append(reformed_event)

        return True, 200, ['Events Fetched'], eve


def view_global_events(offset: int, limit: int) -> tuple[bool, int, list, list]:
    """
    This function verifies incoming data and fetches global community events
    If any errors arise then relevant error messages are returned.
    """

    offset_verify, offset_error = verify_integer(offset, 0, INFINITY)
    limit_verify, limit_error = verify_integer(limit, 1, 50)

    if False in [offset_verify, limit_verify]:

        all_errors = [offset_error, limit_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, 400, error_messages, []

    with get_db() as session:
        event_result = session.query(
            Event.id, Event.community_id, Event.title, Event.description,
            Event.location, Event.latitude, Event.longitude, Event.datetime, Event.duration
        ).filter(
            Event.community_id == Community.id,
            Community.public
        ).order_by(
            Event.datetime.desc(),
            Event.id.asc()
        ).limit(limit).offset(offset).all()

        event_result = [list(_tuple) for _tuple in event_result]

        eve = []

        for event in event_result:
            event_tag_result = session.query(EventTag.tag_id).filter(
                Event.id == event[0],
                Event.id == EventTag.event_id
            ).all()

            tags = []

            for tag in event_tag_result:
                tags.append(get_tag_name(tag[0]))

            reformed_event = {
                'id': event[0],
                'community_id': event[1],
                'title': event[2],
                'description': event[3],
                'location': event[4],
                'latitude': event[5],
                'longitude': event[6],
                'datetime': event[7].strftime("%Y-%m-%d %H:%M:%S"),
                'duration': event[8],
                'tags': tags
            }

            eve.append(reformed_event)

        return True, 200, ['Events Fetched'], eve
