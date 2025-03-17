import http
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from backend.common.middleware.auth import auth_required
from backend.common.proto.accounts_pb2 import UpdateRequest, Response
from backend.common.services import AccountsClient


@auth_required(roles_required=["admin"])
def update_account(request: WSGIRequest):
    """
    Update someone else's account
    """
    client = AccountsClient()

    try:
        data = json.loads(request.body)

        user = data['user']

        if 'new_password' not in data:
            data['new_password'] = ""

        req = UpdateRequest(
            user=user,
            password="",
            new_password=data['new_password'],
            skip_email=True,
            otp="",  # Don't need OTP for admin actions
            is_self=False,
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Data'}, status=http.HTTPStatus.BAD_REQUEST)

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

    print(http_res)
    return JsonResponse(http_res, status=res.http_status)
