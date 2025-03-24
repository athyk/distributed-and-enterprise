import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_searching_pb2
from backend.common.services.community.search import CommunitySearchingClient


@csrf_exempt
def fetch_communities(request: WSGIRequest):
    """
    URL: localhost:8000/community/search

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = CommunitySearchingClient()

    try:
        req = community_searching_pb2.Filter(
            is_with=bool(request.GET.get('is_with', 'False')),
            name=request.GET.get('offset', ''),
            public=int(request.GET.get('offset', '0')),
            minimum_members=int(request.GET.get('offset', '0')),
            tags=request.GET.get('offset', []),
            degrees=request.GET.get('offset', [])
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_searching_pb2.CommunityFilter = client.search(req)
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        'communities': None
    })
