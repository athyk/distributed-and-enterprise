import http
import json
import os

import grpc
from google.protobuf.json_format import MessageToDict
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_announcement_pb2, community_announcement_pb2_grpc


@csrf_exempt
def community_announcement_action_paths(request: WSGIRequest, community_id, announcement_id):
    """
    URL: localhost:8000/community/<int:community_id>/announcements/<int:announcement_id>

    Depending on the request method used defines whether the Update or Delete function is executed
    """

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    if request.method == 'GET':
        return community_announcement_view_single(request, community_id, announcement_id)
    if request.method == 'PUT':
        return community_announcement_edit(request, community_id, announcement_id)
    elif request.method == 'DELETE':
        return community_announcement_delete(request, community_id, announcement_id)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    

@csrf_exempt
def community_announcement_paths(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/announcements

    Depending on the request method used defines whether the Create or View function is executed
    """

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    if request.method == 'GET':
        return community_announcement_view(request, community_id)
    elif request.method == 'POST':
        return community_announcement_creation(request, community_id)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def community_announcement_creation(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/announcements

    Sends a request to the community server with the relevant data to create a new community
    """

    validations = ['user_id', 'title', 'description', 'tags']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.CommunityAnnouncementResponse = stub.CommunityCreateAnnouncement(community_announcement_pb2.CommunityAnnouncementCreateRequest(
        community_id=community_id,
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        tags=data['tags']
    ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def community_announcement_view(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/announcements

    Sends a request to the community server with the relevant data to create a new community
    """

    validations = ['user_id', 'offset', 'limit']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.AllCommunityAnnouncementResponse = stub.CommunityViewSelectAnnouncement(community_announcement_pb2.CommunityAnnouncementViewSelectRequest(
        community_id=community_id,
        user_id=data['user_id'],
        offset=data['offset'],
        limit=data['limit']
    ))

    all_announcements = []

    for announcement in response.announcements:

        json_announcement = MessageToDict(announcement)

        reformed_announcement = {
                "id": json_announcement['id'],
                "title": json_announcement['title'],
                "description": json_announcement['description'],
                "tags": json_announcement.get('tags', []),
                "user_id": json_announcement['userId'],
                "uploaded": json_announcement['uploaded'],
                "edit_user_id": json_announcement.get('editUserId', 0),
                "edit_uploaded": json_announcement.get('editUploaded', None)
            }
        
        all_announcements.append(reformed_announcement)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        "announcements": all_announcements
    })


def community_announcement_view_single(request: WSGIRequest, community_id, announcement_id):
    """
    Sends a request to the community server with the relevant data to fetch a community's data
    """

    validations = ['user_id']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.CommunityAnnouncementResponse = stub.CommunityViewSelectAnnouncement(community_announcement_pb2.CommunityAnnouncementUpdateRequest(
        announcement_id=announcement_id,
        community_id=community_id,
        user_id=data['user_id']
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


@csrf_exempt
def community_global_announcement_view(request: WSGIRequest):
    """
    URL: localhost:8000/community/announcements

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    validations = ['offset', 'limit']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.GlobalCommunityAnnouncementResponse = stub.CommunityViewGlobalAnnouncement(community_announcement_pb2.CommunityAnnouncementGlobalRequest(
        offset=data['offset'],
        limit=data['limit']
    ))

    all_announcements = []

    for announcement in response.global_announcements:

        json_announcement = MessageToDict(announcement)

        print(json_announcement)

        reformed_announcement = {
                "id": json_announcement['id'],
                "title": json_announcement['title'],
                "description": json_announcement['description'],
                "tags": json_announcement.get('tags', []),
                "user_id": json_announcement['userId'],
                "uploaded": json_announcement['uploaded'],
                "edit_user_id": json_announcement.get('editUserId', 0),
                "edit_uploaded": json_announcement.get('editUploaded', None),
                "community_id": json_announcement['communityId']
            }

        all_announcements.append(reformed_announcement)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        "global_announcements": all_announcements
    })


def community_announcement_edit(request: WSGIRequest, community_id, announcement_id):
    """
    Sends a request to the community server with the relevant data to update a community's data
    """

    validations = ['user_id', 'title', 'description', 'tags']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.CommunityAnnouncementResponse = stub.CommunityUpdateAnnouncement(community_announcement_pb2.CommunityAnnouncementUpdateRequest(
        announcement_id=announcement_id,
        community_id=community_id,
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        tags=data['tags']
    ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def community_announcement_delete(request: WSGIRequest, community_id, announcement_id):
    """
    Sends a request to the community server with the relevant data to delete a community
    """

    validations = ['user_id']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("community-service:" + os.environ.get('COMMUNITY_PORT', '50052'))
    stub = community_announcement_pb2_grpc.CommunityAnnouncementStub(channel)
    response: community_announcement_pb2.CommunityAnnouncementResponse = stub.CommunityDeleteAnnouncement(community_announcement_pb2.CommunityAnnouncementDeleteRequest(
        announcement_id=announcement_id,
        community_id=community_id,
        user_id=data['user_id']
    ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })
