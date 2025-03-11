from functools import wraps

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from backend.common.services import AccountsClient


def auth_required(
        redirect_url=None,
        roles_required=None,
        community_roles_required=None,
        redirect_user=False
):
    """
    Decorator to check if a user is authenticated and has the required roles.
    :param redirect_url:  URL to redirect to if the user is not authenticated or does not have the required roles.
    :param roles_required: List of roles required to access the view. Like ['admin', 'moderator']
    :param community_roles_required: List of community roles required to access the view. Like ['cadmin', 'cmoderator']
    :param redirect_user:  If True, the user will be redirected to the redirect_url. If False, the user will be returned a 403.
    :return:
    """
    def redirect_or_return(request: WSGIRequest, redirect_to: str):
        if redirect_user:
            request.session['next_url'] = request.path
            return redirect(redirect_to)
        return JsonResponse(
            {'success': False, 'error': 'Not authenticated'},
            status=403
        )

    def decorator(view_func):
        @wraps(view_func)
        async def _wrapped_view(request: WSGIRequest, *args, **kwargs):
            print(request.COOKIES)
            user: dict | None = AccountsClient().check_session(request.COOKIES.get('sid'))

            redirect_to = redirect_url or settings.LOGIN_URL

            if user is None:
                print("User is not authenticated or session expired")
                return redirect_or_return(request, redirect_to)

            allowed = False
            if roles_required is not None:
                if user['rank'] in roles_required:
                    allowed = True

            if community_roles_required is not None:
                # TODO: Implement community roles
                pass

            if not allowed:
                print("User does not have the required roles")
                return redirect_or_return(request, redirect_to)

            # view func is the next function to be called
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

