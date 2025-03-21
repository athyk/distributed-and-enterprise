import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from backend.common.proto.degree_pb2 import DegreeDeleteRequest, DegreeDeleteResponse
from backend.common.services import DegreesClient


def delete_degree(request: WSGIRequest):
    """
    Deletes a degree
    """
    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = DegreesClient()

    try:
        data = json.loads(request.body)

        req = DegreeDeleteRequest(
            id=int(data['id'])
        )
    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: DegreeDeleteResponse = client.delete(req)
    except Exception as e:
        traceback.print_exc()
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
