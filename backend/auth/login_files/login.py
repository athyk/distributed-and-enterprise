from backend.common.utils import verify_string, verify_boolean, verify_list, verify_integer
from backend.community.database.database import get_db
from werkzeug.security import check_password_hash


def user_login(email: str, password: str) -> tuple[bool, int, list]:
    email_verify, email_error = verify_string(email, 4, 64)
    password_verify, password_error = verify_string(password, 8, 32)

    if False in [email_verify, password_verify]:

        all_errors = [email_error, password_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages

    with get_db() as session:
        user = session.query(User).filter(User.email == email).first()

        if not user:
            return False, -1, ['Invalid Email Or Password']

        pass_correct = check_password_hash(user.password, password)

        if not pass_correct:
            return False, -1, ['Invalid Email Or Password']

        return True, user.id, []
