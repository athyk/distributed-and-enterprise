import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from backend.common.middleware.auth import auth_required
from backend.common.proto.account_post_pb2 import AccountPostUpdateRequest, AccountPostResponse
from backend.common.services import AccountPostsClient, AccountsClient


@auth_required()
def update_post(request: WSGIRequest):
    """
    Updates a post
    """
    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AccountsClient()
    user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    client = AccountPostsClient()

    try:
        data = json.loads(request.body)

        req = AccountPostUpdateRequest(
            post_id=data.get('post_id'),
            user_id=user['id'],
            title=data.get('title', ''),
            description=data.get('description', ''),
            tags=data.get('tags', []),
            images=data.get('images', []),
        )
    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: AccountPostResponse = client.update(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if res.post.id > 0:
        http_res['post'] = client.post_to_json(res.post)

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
