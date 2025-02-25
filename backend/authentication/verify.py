from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.authentication.email import send_verification_code_email
import pyotp
import os
import json
import uuid

def create_otp():
    """Create OTP Codes"""
    otp_id = uuid.uuid4().int
    hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'),digits=6)
    code = hotp.at(otp_id)
    return code,otp_id,hotp.verify(code, otp_id)

@csrf_exempt
def verify_otp(request):
    """Verify OTP Codes"""
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if not all([data.get('otp'), data.get('id')]):
            return JsonResponse({"error": "All fields are required","valid": False}, status=400)

        if type(data.get('id')) != int:
            return JsonResponse({"error": "Invalid Param","valid": False}, status=400)

        if type(data.get('otp')) != int:
            return JsonResponse({"error": "Invalid Param","valid": False}, status=400)

        otp = data.get('otp')
        id = data.get('id')

        hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'))
        if not hotp.verify(otp, id):
            return JsonResponse({"error": "Invalid OTP","valid": False}, status=400)
        return JsonResponse({"message": "OTP verified","valid": True}, status=200)
    return JsonResponse({"error": "Invalid request method","valid": False}, status=405)

@csrf_exempt
def send_verifcation_code(request):
    """Send Verification Code to email"""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data.get("email")
            skip_email = data.get("skip_email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            code, id, verified = create_otp()
            if not verified:
                return JsonResponse({"error": "OTP Generation Error"}, status=400)

            if skip_email:
                return JsonResponse({"message": f"Verification code sent successfully {code}","ID": id}, status=200)

            send_email = send_verification_code_email("SENDGRID_EMAIL", email, code)

            if send_email[1] == 500:
                return JsonResponse({"error": send_email[0]}, status=500)

            return JsonResponse({"message": "Verification code sent successfully","ID": id}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
