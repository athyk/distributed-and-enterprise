import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from backend.common.middleware.auth import auth_required
from backend.common.proto.account_post_pb2 import AccountPostGetRequest, AccountPostResponse
from backend.common.services import AccountPostsClient, AccountsClient


@auth_required()
def delete_post(request: WSGIRequest):
    """
    Deletes a post
    """
    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AccountsClient()
    user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    client = AccountPostsClient()

    if user['rank'] == 'admin' or user['rank'] == 'moderator':
        user['id'] = -1  # Mark them as an admin - used for performance.

    try:
        data = json.loads(request.body)

        req = AccountPostGetRequest(
            post_id=int(data['id']),
            user_id=int(user['id']),
        )
    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: AccountPostResponse = client.delete(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
