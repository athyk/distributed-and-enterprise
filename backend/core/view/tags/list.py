import http
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.tag_pb2 import TagListRequest, TagListResponse
from backend.common.services import TagsClient


def list_tags(request: WSGIRequest):
    """
    List most tags/search tags
    """
    client = TagsClient()

    try:
        req = TagListRequest(
            page=int(request.GET.get('page', 0)),
            limit=int(request.GET.get('limit', 50)),
            name=request.GET.get('name', ''),
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: TagListResponse = client.list(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.tags) > 0:
        http_res['tags'] = []
        for tag in res.tags:
            http_res['tags'].append(client.tag_to_json(tag))

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
