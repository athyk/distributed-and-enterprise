import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.middleware.auth import auth_required
from backend.common.services import AccountsClient


@auth_required()
@csrf_exempt
def logout_self(request: WSGIRequest):
    """
    Log the user out of the system or invalidate the session
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = AccountsClient()
    real_user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not real_user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    try:
        if bool(request.GET.get('all', False)):
            res = client.logout_user(real_user["id"])
        else:
            res = client.logout_session(request.COOKIES.get('sid'))
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res,
    }

    return JsonResponse(http_res, status=http.HTTPStatus.OK)
