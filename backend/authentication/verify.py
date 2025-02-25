from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyotp
import os
import json
import uuid

def create_otp():
    otp_id = uuid.uuid4().int
    hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'),digits=6)
    code = hotp.at(otp_id)
    return code,otp_id,hotp.verify(code, otp_id)

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if not all([data.get('otp'), data.get('id')]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        if type(data.get('id')) != int:
            return JsonResponse({"error": "Invalid Param"}, status=400)

        if type(data.get('otp')) != int:
            return JsonResponse({"error": "Invalid Param"}, status=400)

        otp = data.get('otp')
        id = data.get('id')

        hotp = pyotp.HOTP(os.environ.get('OTP_SECRET'))
        if not hotp.verify(otp, id):
            return JsonResponse({"error": "Invalid OTP"}, status=400)
        return JsonResponse({"message": "OTP verified"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)