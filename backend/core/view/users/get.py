import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.accounts_pb2 import GetRequest, GetResponse
from backend.common.services import AccountsClient


def get_accounts(request: WSGIRequest):
    """
    Get account(s)
    """
    client = AccountsClient()
    try:

        req = GetRequest(  # TODO: Search by age etc
            user_id=request.GET.get('user_id', 0),
            email='',  # TODO: Admin only
            first_name=request.GET.get('first_name', ''),
            last_name=request.GET.get('last_name', ''),
            email_verified=0,  # TODO: Admin only
            age_from=int(request.GET.get('age_from', 0)),
            age_to=int(request.GET.get('age_to', 0)),
            degree_id=int(request.GET.get('degree_id', 0)),
            tag_id=int(request.GET.get('tag_id', 0)),
            gender=request.GET.get('gender', ''),
            year_of_study=int(request.GET.get('year_of_study', 0)),
            page=request.GET.get('page', 0),
            limit=request.GET.get('limit', 50),
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: GetResponse = client.get(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.users) > 0:
        http_res['users'] = []
        for user in res.users:
            user.email = ''  # Prevents leaking emails, passwords are not exposed anyway
            http_res['users'].append(client.user_to_json(user))

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    print(http_res)
    return JsonResponse(http_res, status=res.http_status)
