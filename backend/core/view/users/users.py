import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.middleware.auth import auth_required
from backend.core.view.users.delete import delete_accounts
from backend.core.view.users.get import get_accounts
from backend.core.view.users.update import update_account


@auth_required()
@csrf_exempt
def user_paths(request: WSGIRequest):
    """
    All paths related to users
    """
    if request.method == 'DELETE':
        return delete_accounts(request)
    elif request.method == 'GET':
        return get_accounts(request)
    elif request.method == 'PUT':
        return update_account(request)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
