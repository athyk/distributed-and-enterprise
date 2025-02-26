from backend.common.files.data_verify import verify_string, verify_boolean, verify_list, verify_integer
from backend.community.database.database import get_db
from backend.community.database.models import Community, CommunityUser

from backend.community.crud.local_functions import add_tags, add_degrees

from math import inf as INFINITY

def create_community(name, description, public, tags, degrees, user_id):
    name_verify, name_error = verify_string(name, 4, 64)
    description_verify, description_error = verify_string(description, 4, 511)
    public_verify, public_error = verify_boolean(public)
    tags_verify, tags_error = verify_list(tags, 0, 5)
    degrees_verify, degrees_error = verify_list(degrees, 0, 5)
    user_verify, user_error = verify_integer(user_id, 1, INFINITY)

    if False in [name_verify, description_verify, public_verify, tags_verify, degrees_verify, user_verify]:

        all_errors = [name_error, description_error, public_error, tags_error, degrees_error, user_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages

    with get_db() as session:
        result = session.query(Community.id).filter(Community.name == name).all()

        if result:
            return False, -1, [f'You cannot create a community using a name that is already taken. Provided Name: {name}']

        new_community = Community(
            name=name, 
            description=description, 
            public=public
        )

        session.add(new_community)
        session.commit()

        new_community_id = new_community.id
        further_non_critical_errors = ['Community Successfully Created']

        further_non_critical_errors = add_tags(session, tags, new_community_id, further_non_critical_errors)
        further_non_critical_errors = add_degrees(session, degrees, new_community_id, further_non_critical_errors)

        new_admin = CommunityUser(
            community_id=new_community_id,
            user_id=user_id,
            role='Admin'
        )

        session.add(new_admin)
        session.commit()

        return True, new_community_id, further_non_critical_errors
