import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.common.proto.accounts_pb2 import LoginRequest, LoginResponse
from backend.common.services import AccountsClient


@csrf_exempt
def login_user(request: WSGIRequest):
    """
    Logs into an existing user account
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error_message': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AccountsClient()

    try:
        data = json.loads(request.body)

        if 'skip_email' not in data:
            data['skip_email'] = False

        if 'otp' not in data:
            data['otp'] = ""

        req = LoginRequest(
            email=data['email'],
            password=data['password'],
            skip_email=data['skip_email'],
            otp=data['otp'],
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: LoginResponse = client.login(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
        'user_id': res.user_id
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    # user is filled out but left empty, even if the user is not created.
    # so check id, as it's the only required field.
    if res.user.id != 0:
        http_res['user'] = client.user_to_json(res.user)

    if res.otp_required:
        http_res['otp_required'] = res.otp_required

    response = JsonResponse(http_res, status=res.http_status)

    if res.success and res.user.id != 0:
        session_id, max_age = client.create_session(res.user)
        response.set_cookie(
            'sid',
            session_id,
            max_age=max_age,
            secure=False,  # Changing this to True would only allow this to work over HTTPS and not HTTP
            httponly=True  # Makes it so client side code cannot see the cookie
        )

    return response
