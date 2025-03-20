import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_joins_pb2
from backend.common.services.community.joins import CommunityJoinsClient


@csrf_exempt
def join_community(request: WSGIRequest, community_id: int):
    """
    URL: localhost:8000/community/<int:community_id>/members

    Sends a request to the community server with the relevant data to join the community
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = CommunityJoinsClient()

    try:
        req = community_joins_pb2.CommunityActionRequest(
            community_id=community_id
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_joins_pb2.CommunityActionResponse = client.join(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })
