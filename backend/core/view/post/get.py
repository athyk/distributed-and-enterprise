import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.account_post_pb2 import AccountPostGetRequest, AccountPostResponse
from backend.common.proto.accounts_pb2 import GetRequest
from backend.common.services import AccountPostsClient, AccountsClient
from backend.core.utils import get_tag_name


def get_post(request: WSGIRequest):
    """
    Get a specific post
    """
    client = AccountPostsClient()
    user_client = AccountsClient()

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
        json_post = client.post_to_json(res.post)
        json_post['tags'] = [get_tag_name(tag) for tag in json_post['tags']]

        req_user = GetRequest(user_id = json_post['user_id'])
        user_result = user_client.get(req_user)

        user_data = {
            'user_id': user_result.users[0].id,
            'first_name': user_result.users[0].first_name,
            'last_name': user_result.users[0].last_name,
            'picture_url': user_result.users[0].picture_url
        }

        del json_post['user_id']

        json_post['user_data'] = user_data

        http_res['post'] = json_post

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
