import http
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.accounts_pb2 import UpdateRequest, Response
from backend.common.services import AccountsClient


def update_self_account(request: WSGIRequest):
    """
    Update the user's own account
    """
    client = AccountsClient()
    real_user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not real_user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    try:
        data = json.loads(request.body)

        if 'skip_email' not in data:
            data['skip_email'] = False

        if 'otp' not in data:
            data['otp'] = ""

        if 'password' not in data:
            data['password'] = ""

        if 'new_password' not in data:
            data['new_password'] = ""

        user = data['user']

        user["id"] = real_user["id"]

        if "rank" in user:
            return JsonResponse({'success': False, 'error_message': "Cannot change your account level"}, status=http.HTTPStatus.UNAUTHORIZED)

        req = UpdateRequest(
            user=data['user'],
            password=data['password'],
            new_password=data['new_password'],
            skip_email=data['skip_email'],
            otp=data['otp'],
            is_self=True,
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: Response = client.update(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if res.otp_required:
        http_res['otp_required'] = True

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
