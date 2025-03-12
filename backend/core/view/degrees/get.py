import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.degree_pb2 import DegreeGetRequest, DegreeGetResponse
from backend.common.services import DegreesClient


def get_degrees(request: WSGIRequest):
    """
    Get a specific degree
    """
    client = DegreesClient()

    try:
        req = DegreeGetRequest(
            id=int(request.GET.get('id', 0)),
            name=request.GET.get('name', ""),
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: DegreeGetResponse = client.get(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if res.degree.id > 0:
        http_res['degree'] = client.degree_to_json(res.degree)

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    print(http_res)
    return JsonResponse(http_res, status=res.http_status)
