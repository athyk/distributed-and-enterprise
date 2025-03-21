import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from backend.common.proto.accounts_pb2 import GetRequest, GetResponse
from backend.common.services import AccountsClient


def get_self(request: WSGIRequest):
    """
    Get the user's own account
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'GET method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = AccountsClient()
    user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    try:
        req = GetRequest(
            user_id=user['id'],
        )
        res: GetResponse = client.get(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    if len(res.users) > 0:
        http_res['user'] = client.user_to_json(res.users[0])
    else:
        return JsonResponse({'success': False, "error_message": "No User Found"}, status=http.HTTPStatus.BAD_REQUEST)

    return JsonResponse(http_res, status=res.http_status)


