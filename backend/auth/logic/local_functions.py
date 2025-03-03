import uuid


def generate_id() -> tuple[str, bool]:
    """
    This function generates a UUIDv4 for the user.

    v7 would have been used but the standard lib does not support it.
    """
    try:
        # str since it's an uuid.UUID type
        return str(uuid.uuid4()), False
    except Exception:  # pragma: no cover
        # too many exceptions to catch, so we catch all.
        # And coverage ignore since it may be too hard to test in a normal environment.
        return "", False


def ensure_valid_otp(user_id: str, otp: str) -> bool:
    # TODO: Implement this
    """
    This function checks if the OTP is valid.

    :param user_id:
    :param otp:
    :return:
    """
    # OTP is 6 digits
    if len(otp) != 6:
        return False

    return True