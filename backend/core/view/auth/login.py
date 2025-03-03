import http
import json
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto.auth_pb2 import *
from backend.common.services import AuthClient



@csrf_exempt
def login_user(request: WSGIRequest):
    """
    Logs into an existing user account
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error_message': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AuthClient()

    try:
        data = json.loads(request.body)

        if 'skip_email' not in json.loads(request.body):
            data['skip_email'] = False

        req = LoginRequest(
            email=data['email'],
            password=data['password'],
            skip_email=data['skip_email']
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception as e:  # Occurs if the JSON is valid but the data is not
        # While a loop seems better, this is faster.

        data = json.loads(request.body)
        if 'email' not in data:
            return JsonResponse({'success': False, 'error_message': f'Key: email Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

        if 'password' not in data:
            return JsonResponse({'success': False, 'error_message': f'Key: password Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

        print(e)
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: LoginResponse = client.login_user(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
        'user_id': res.user_id
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    # user is always filled out, even if the user is not created.
    # so check id, as it's the only required field.
    if res.user.id != "":
        http_res['user'] = client.user_to_json(res.user)

    if res.otp_required:
        http_res['otp_required'] = res.otp_required

    return JsonResponse(http_res, status=res.http_status)
