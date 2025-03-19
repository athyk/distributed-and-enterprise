import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.middleware.auth import auth_required
from backend.core.view.users.self.delete_self import delete_self_account
from backend.core.view.users.self.get_self import get_self
from backend.core.view.users.self.update_self import update_self_account


@auth_required()
@csrf_exempt
def user_self_paths(request: WSGIRequest):
    """
    All paths related to users
    """
    if request.method == 'DELETE':
        return delete_self_account(request)
    elif request.method == 'GET':
        return get_self(request)
    elif request.method == 'PUT':
        return update_self_account(request)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
