from backend.common.utils import verify_string
from backend.auth.database.database import get_db
from werkzeug.security import check_password_hash
from math import inf as INFINITY

from backend.auth.database.models import User


def user_login(email: str, password: str) -> tuple[bool, int, list]:
    """
    This function with the given data logs in the user if the account is verified.
    If any errors arise then relevant error messages are returned.
    """

    email_verify, email_error = verify_string(email, 4, 255) # Cannot exceed 255 rfc3696
    password_verify, password_error = verify_string(password, 8, INFINITY)

    if False in [email_verify, password_verify]:

        all_errors = [email_error, password_error]
        error_messages = [item for item in all_errors if item.strip()]

        return False, -1, error_messages

    with get_db() as session:
        user = session.query(User.id, User.password, User.account_verified).filter(User.email == email).first()

        if user is None:
            return False, -1, ['Invalid Email Or Password']

        pass_correct = check_password_hash(user[1], password)

        if not pass_correct:
            return False, -1, ['Invalid Email Or Password']
        
        if not user[2]:
            return False, user[0], ['Account Not Verified By Email']

        return True, user[0], []
