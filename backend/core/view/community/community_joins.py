import http
import json
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_joins_pb2
from backend.common.services.community.joins import CommunityJoinsClient


@csrf_exempt
def community_join_actions(request: WSGIRequest, community_id: int):
    """
    URL: localhost:8000/community/<int:community_id>/members

    Sends a request to the community server with the relevant data to join the community
    """

    if request.method == 'POST':
        return join_community(request, community_id)

    elif request.method == 'DELETE':
        return leave_community(request, community_id)

    elif request.method == 'GET':
        return with_community(request, community_id)

    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def join_community(request: WSGIRequest, community_id: int):
    """
    URL: localhost:8000/community/<int:community_id>/members

    Sends a request to the community server with the relevant data to join the community
    """

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


def leave_community(request: WSGIRequest, community_id: int):
    """
    URL: localhost:8000/community/<int:community_id>/members

    Sends a request to the community server with the relevant data to leave a community
    """

    client = CommunityJoinsClient()

    try:
        req = community_joins_pb2.CommunityActionRequest(
            community_id=community_id
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_joins_pb2.CommunityActionResponse = client.leave(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def with_community(request: WSGIRequest, community_id: int):
    """
    URL: localhost:8000/community/<int:community_id>/members

    Sends a request to the community server with the relevant data to leave a community
    """

    client = CommunityJoinsClient()

    try:
        req = community_joins_pb2.CommunityActionRequest(
            community_id=community_id
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_joins_pb2.CommunityActionResponse = client.is_with(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })
