from backend.common.utils import verify_string, verify_list, verify_integer
from backend.auth.database.database import get_db
from werkzeug.security import generate_password_hash
from datetime import datetime

from backend.auth.database.models import User, Degree
from backend.auth.login_files.local_functions import add_tags


def register_user(
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        dob: str,
        gender: str,
        degree: str,
        year_of_study: int,
        grad_year: str,
        tags: list
        ) -> tuple[bool, int, list]:
    """
    This function takes in data and registers a user into the database.
    If any errors arise then relevant error messages are returned.
    """

    email_verify,         email_error         = verify_string(email, 4, 64)
    password_verify,      password_error      = verify_string(password, 8, 32)
    first_name_verify,    first_name_error    = verify_string(first_name, 2, 48)
    last_name_verify,     last_name_error     = verify_string(last_name, 2, 48)
    dob_verify,           dob_error           = verify_string(dob, 10, 10)
    gender_verify,        gender_error        = verify_string(gender, 4, 12)
    degree_verify,        degree_error        = verify_string(degree, 4, 128)
    year_of_study_verify, year_of_study_error = verify_integer(year_of_study, 1, 9)
    grad_year_verify,     grad_year_error     = verify_string(grad_year, 10, 10)
    tag_verify,           tag_error           = verify_list(tags, 0, 5)

    if False in [email_verify, password_verify, first_name_verify, last_name_verify ,dob_verify,
                 gender_verify, degree_verify, year_of_study_verify, grad_year_verify, tag_verify]:

        all_errors = [email_error, password_error, first_name_error, last_name_error, dob_error,
                      gender_error, degree_error, year_of_study_error, grad_year_error, tag_error]

        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages
    
    print('Verify')

    with get_db() as session:
        print('searching')
        user = session.query(User).filter(User.email == email).first()

        print('User searched')
        print(user)

        if user:
            return False, -1, ['Email Already In Use']

        try:
            dob_obj = datetime.strptime(dob, "%d-%m-%Y").date()
            grad_year_obj = datetime.strptime(grad_year, "%d-%m-%Y").date()
        
        except Exception:
            return False, -1, ['Dates Not Formatted Correctly']
        
        degree_id = session.query(Degree.id).filter(Degree.name == degree).first()

        print('degree searched')

        if degree_id is None:
            return False, -1, ['Degree Provided Does Not Exist']

        hashed_password = generate_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=dob_obj,
            gender=gender,
            degree=degree_id[0],
            year_of_study=year_of_study,
            grad_year=grad_year_obj,
            created_at=datetime.utcnow(),
            updated_at=None,
            picture_url=None,
            two_fa_secret=None
        )

        session.add(new_user)
        session.commit()

        further_non_critical_errors = ['User Successfully Created. Email Verification Required.']
        further_non_critical_errors = add_tags(session, tags, new_user.id, further_non_critical_errors)

        return True, new_user.id, further_non_critical_errors
