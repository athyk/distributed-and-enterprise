import http
import json
import os
import traceback

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_pb2, community_pb2_grpc
from backend.common.proto.community_pb2 import CommunityCreateRequest, CommunityUpdateRequest, CommunityViewRequest, \
    CommunityDeleteRequest, CommunityIDResponse, CommunityDataResponse, BasicCommunityResponse

from backend.common.services.community.community import CommunityClient


@csrf_exempt
def community_crud_paths(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/

    Depending on the request method used defines whether the Read, Update or Delete function is executed
    """

    if request.method == 'GET':
        return community_read(request, community_id)
    elif request.method == 'PUT':
        return community_update(request, community_id)
    elif request.method == 'DELETE':
        return community_delete(request, community_id)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def community_creation(request: WSGIRequest):
    """
    URL: localhost:8000/community/

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    validations = ['name', 'description', 'public', 'tags', 'degrees']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    client = CommunityClient()

    try:
        data = json.loads(request.body)

        req = CommunityCreateRequest(
            name=data['name'],
            description=data['description'],
            public=data['public'],
            tags=data['tags'],
            degrees=data['degrees']
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: CommunityIDResponse = client.create(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'id': response.id
    })


def community_read(request: WSGIRequest, community_id):
    """
    Sends a request to the community server with the relevant data to fetch a community's data
    """

    client = CommunityClient()

    try:
        req = CommunityViewRequest(
            id=community_id
        )

    except Exception as e:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: CommunityDataResponse = client.view(req)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'name': response.name,
        'description': response.description,
        'public_community': response.public_community,
        'tags': list(response.tags),
        'degrees': list(response.degrees)
    })


def community_update(request: WSGIRequest, community_id):
    """
    Sends a request to the community server with the relevant data to update a community's data
    """

    client = CommunityClient()

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)
    
    validations = ['name', 'description', 'public', 'tags', 'degrees']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        data = json.loads(request.body)

        req = CommunityUpdateRequest(
            id=community_id,
            name=data['name'],
            description=data['description'],
            public=data['public'],
            tags=data['tags'],
            degrees=data['degrees']
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: BasicCommunityResponse = client.update(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def community_delete(request: WSGIRequest, community_id):
    """
    Sends a request to the community server with the relevant data to delete a community
    """

    client = CommunityClient()

    try:
        req = CommunityDeleteRequest(
            id=community_id
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: BasicCommunityResponse = client.delete(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })
