import http
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.degree_pb2 import DegreeListRequest, DegreeListResponse
from backend.common.services import DegreesClient


def list_degrees(request: WSGIRequest):
    """
    List most degrees/search degrees
    """
    client = DegreesClient()

    try:
        req = DegreeListRequest(
            page=int(request.GET.get('page', 0)),
            limit=int(request.GET.get('limit', 50)),
            name=request.GET.get('name', ''),
        )
    except Exception:
        return JsonResponse({'success': False, 'error_message': 'Invalid Query'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: DegreeListResponse = client.list(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.degrees) > 0:
        http_res['degrees'] = []
        for degree in res.degrees:
            http_res['degrees'].append(client.degree_to_json(degree))

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
