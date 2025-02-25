import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.validators import RegexValidator

def check_email(email):
    email_validator = RegexValidator(
        regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        message="Enter a valid email address.",
        code="invalid_email",
    )
    try:
        email_validator(email)
    except Exception as e:
        return e.message, 500
    return email


def send_verification_code_email(send_id, user_email):
    from_email = check_email(os.environ.get(send_id))
    if from_email[1] == 500:
        return "Invalid email", 500

    to_email = check_email(user_email)
    if to_email[1] == 500:
        return "Invalid email", 500
    try:
        message = Mail(
            from_email=from_email,
            to_emails=user_email,
            subject='Sending with Twilio SendGrid is Fun',
            html_content='<strong>and easy to do anywhere, even with Python</strong>')
    except Exception as e:
        return e.message, 500
    print(message)

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        return e.message, 500
    return "Email sent successfully", 200