import traceback

import pyotp
import os
import uuid

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from backend.accounts.database.models import User
from backend.accounts.database.database import get_db


def create_otp():
    """Create OTP Codes"""
    otp_id = uuid.uuid4().int
    hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'),digits=6)
    code = hotp.at(otp_id)
    return code, otp_id, hotp.verify(code, otp_id)


def load_html_template(file_path, code):
    """Load HTML file and replace the OTP placeholder."""

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content.replace("123456", str(code))


def send_verification_code_email(user_email: str) -> tuple[bool, str, int]:
    """Send Verification Code to email"""
    try:
        code, otp_seed, valid = create_otp()

        if not valid:
            return False, 'System Error Occurred', -1
    except Exception:
        traceback.print_exc()
        return False, 'System Error Occurred', -1

    try:
        html_template = load_html_template("backend/accounts/verification/email.html", code)
        message = Mail(
            from_email='auth@xavierlloyd.dev',
            to_emails=user_email,
            subject='UniHub Email Verification',
            html_content=html_template
            )
    except Exception:
        traceback.print_exc()
        return False, 'Unable to create email message', -1

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception:
        traceback.print_exc()
        return False, 'Verification message failed to send', -1

    return True, "Email sent successfully", otp_seed


def verify_email(otp: str, email_verify_id: str, user_email: str) -> tuple[bool, str]:
    """This function verifies if the code that the user inputted is correct, thus validating their account"""
    hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'))

    if not hotp.verify(otp, int(email_verify_id)):
        return False, "Invalid OTP Code Provided"

    with get_db() as session:
        user = session.query(User).filter(User.email == user_email).first()

        if user is None:
            return False, "User Does Not Exist"

        user.email_verified = True

        session.commit()
        
        return True, "Account Verified"
