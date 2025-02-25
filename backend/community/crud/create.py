from backend.common.files.data_verify import verify_string
#from backend.community.database.models import User, SessionLocal


def create_community(name, description, public, tags, degrees):

    name_verify, name_error = verify_string(name, 4, 32)
    description_verify, description_error = verify_string(description, 4, 6)

    if False in [name_verify, description_verify]:

        all_errors = [name_error, description_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages
    


    


    
    
    return False, 0, "Failed"

