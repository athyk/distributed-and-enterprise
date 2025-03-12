import http
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.tag_pb2 import TagGetRequest, TagGetResponse
from backend.common.services import TagsClient


def get_tags(request: WSGIRequest):
    """
    Get a specific tag
    """
    client = TagsClient()

    try:
        req = TagGetRequest(
            id=int(request.GET.get('id', 0)),
            name=request.GET.get('name', ""),
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: TagGetResponse = client.get(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if res.tag.id > 0:
        http_res['tag'] = client.tag_to_json(res.tag)

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    print(http_res)
    return JsonResponse(http_res, status=res.http_status)
