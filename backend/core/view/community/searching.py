import http
import traceback

from google.protobuf.json_format import MessageToDict
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
        tags = request.GET.get('tags', [])
        degrees = request.GET.get('degrees', [])

        tags = [int(x) for x in tags]
        degrees = [int(x) for x in degrees]

        req = community_searching_pb2.Filter(
            is_with=int(request.GET.get('is_with', '0')),
            name=request.GET.get('name', ''),
            public=int(request.GET.get('public', '0')),
            minimum_members=int(request.GET.get('minimum_members', '0')),
            tags=tags,
            degrees=degrees,
            offset=int(request.GET.get('offset', '0')),
            limit=int(request.GET.get('limit', '1'))
        )

    except Exception: # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_searching_pb2.CommunityFilter = client.search(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
    
    all_communities = []

    if response.status.success:
        for community in response.communities:
            json_community = MessageToDict(community)

            reformed_community = {
                    "id": json_community['id'],
                    "name": json_community['name'],
                    "description": json_community['description'],
                    "public": True if json_community['publicCommunity'] == 1 else False,
                    "tags": json_community.get('tags', []),
                    "degrees": json_community.get('degrees', []),
                    "member_count": json_community['memberCount']
                }

            all_communities.append(reformed_community)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        'communities': all_communities
    })
