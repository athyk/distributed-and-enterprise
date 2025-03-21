import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.core.view.post.delete import delete_post
from backend.core.view.post.get import get_post
from backend.core.view.post.create import create_post
from backend.core.view.post.update import update_post


@csrf_exempt
def post_paths(request: WSGIRequest):
    """
    All paths related to degrees
    """
    if request.method == 'POST':
        return create_post(request)
    elif request.method == 'DELETE':
        return delete_post(request)
    elif request.method == 'GET':
        return get_post(request)
    elif request.method == 'PUT':
        return update_post(request)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

