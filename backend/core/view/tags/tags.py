import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.core.view.tags.delete import delete_tag
from backend.core.view.tags.get import get_tags


@csrf_exempt
def tag_paths(request: WSGIRequest):
    """
    All paths related to tags
    """

    if request.method == 'DELETE':
        return delete_tag(request)
    elif request.method == 'GET':
        return get_tags(request)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

