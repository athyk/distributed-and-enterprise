import http
import json
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_pb2, community_pb2_grpc

@csrf_exempt
def community_crud_paths(request: WSGIRequest, community_id):
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

    print('\n\n\nMethod Used')
    print(request.method)

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('Community_PORT', '50052'))
    stub = community_pb2_grpc.CommunityStub(channel)
    response: community_pb2.CommunityIDResponse = stub.CommunityCreate(community_pb2.CommunityCreateRequest(
        name = data['name'],
        description = data['description'],
        public = data['public'],
        tags = data['tags'],
        degrees = data['degrees'],
        user_id = data['user_id']
        ))
    
    print(response)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'id': response.id
        })


def community_read(request: WSGIRequest, community_id):
    channel = grpc.insecure_channel("community-service:" + os.environ.get('Community_PORT', '50052'))
    stub = community_pb2_grpc.CommunityStub(channel)
    response: community_pb2.CommunityDataResponse = stub.CommunityView(community_pb2.CommunityViewRequest(
        id = community_id
        ))

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
    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('Community_PORT', '50052'))
    stub = community_pb2_grpc.CommunityStub(channel)
    response: community_pb2.BasicCommunityResponse = stub.CommunityUpdate(community_pb2.CommunityUpdateRequest(
        id = community_id,
        name = data['name'],
        description = data['description'],
        public = data['public'],
        tags = data['tags'],
        degrees = data['degrees'],
        user_id = data['user_id']
        ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
        })


def community_delete(request: WSGIRequest, community_id):
    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('Community_PORT', '50052'))
    stub = community_pb2_grpc.CommunityStub(channel)
    response: community_pb2.BasicCommunityResponse = stub.CommunityDelete(community_pb2.CommunityDeleteRequest(
        id = community_id,
        user_id = data['user_id']
        ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
        })
