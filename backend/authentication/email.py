import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.validators import RegexValidator

def load_html_template(file_path, code):
    """Load HTML file and replace the OTP placeholder."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content.replace("123456", str(code))

def check_email(email): # Probably should make a utils
    """Check if email is valid"""
    email_validator = RegexValidator(
        regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        message="Enter a valid email address.",
        code="invalid_email",
    )
    try:
        email_validator(email)
    except Exception as e:
        return str(e), 500
    return email


def send_verification_code_email(send_id, user_email,code):
    """Send Verification Code to email"""
    from_email = check_email(os.environ.get(send_id))
    if from_email[1] == 500:
        return "Invalid email", 500

    to_email = check_email(user_email)
    if to_email[1] == 500:
        return "Invalid email", 500
    try:
        html_template = load_html_template("backend/authentication/email.html", code)
        message = Mail(
            from_email=from_email,
            to_emails=user_email,
            subject='UniHub Email Verification',
            html_content=html_template
            )
    except Exception as e:
        return e.message, 500
    print(message)

    # Send Email Code Capped at 100 a day


    # try:
    #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #     response = sg.send(message)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     return e.message, 500

    return "Email sent successfully", 200