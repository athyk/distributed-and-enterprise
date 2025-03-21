import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.core.view.degrees.create import create_degree
from backend.core.view.degrees.delete import delete_degree
from backend.core.view.degrees.get import get_degrees


@csrf_exempt
def degree_paths(request: WSGIRequest):
    """
    All paths related to degrees
    """
    if request.method == 'POST':
        return create_degree(request)
    elif request.method == 'DELETE':
        return delete_degree(request)
    elif request.method == 'GET':
        return get_degrees(request)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

