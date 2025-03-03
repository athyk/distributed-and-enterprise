import http
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto.auth_pb2 import LoginVerificationResponse, LoginVerificationRequest
from backend.common.services import AuthClient


@csrf_exempt
def verify(request: WSGIRequest):
    """
    Ensures that the user is verified, by verifying the email otp or totp.

    Used for both registration and login.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error_message': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AuthClient()

    try:
        data = json.loads(request.body)

        req = LoginVerificationRequest(
            user_id=data['user_id'],
            otp=data['otp']
        )
    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception as e:  # Occurs if the JSON is valid but the data is not
        # While a loop seems better, this is faster.
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'success': False, 'error_message': 'Key: user_id Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

        if 'otp' not in data:
            return JsonResponse({'success': False, 'error_message': 'Key: otp Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

        print(e)
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: LoginVerificationResponse = client.verify_login(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
        # No user id, that's sent in the user object
    }

    if len(res.error_message) > 0:
        print(res.error_message)
        http_res['error_message'] = list(res.error_message)

    # user is always filled out, even if the user is not created.
    # so check id, as it's the only required field.
    if res.user.id != "":
        http_res['user'] = client.user_to_json(res.user)

    return JsonResponse(http_res, status=res.http_status)

