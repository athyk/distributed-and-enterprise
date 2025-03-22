import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.account_post_pb2 import AccountPostGetRequest, AccountPostResponse
from backend.common.services import AccountPostsClient


def get_post(request: WSGIRequest):
    """
    Get a specific post
    """
    client = AccountPostsClient()

    try:
        req = AccountPostGetRequest(
            post_id=int(request.GET.get('post_id', 0))
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: AccountPostResponse = client.get(req)
    except Exception as e:
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
