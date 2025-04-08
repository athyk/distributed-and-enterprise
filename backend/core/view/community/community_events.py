import http
import json
import traceback

from google.protobuf.json_format import MessageToDict
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import community_event_pb2
from backend.common.services.community.event import CommunityEventClient


@csrf_exempt
def community_event_action_paths(request: WSGIRequest, community_id, event_id):
    """
    URL: localhost:8000/community/<int:community_id>/events/<int:event_id>

    Depending on the request method used defines whether the Update or Delete function is executed
    """

    if request.method == 'GET':
        return community_event_view_single(request, community_id, event_id)
    elif request.method == 'DELETE':
        return community_event_delete(request, community_id, event_id)

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    if request.method == 'PUT':
        return community_event_edit(request, community_id, event_id)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    

@csrf_exempt
def community_event_paths(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/events

    Depending on the request method used defines whether the Create or View function is executed
    """

    if request.method == 'GET':
        return community_event_view(request, community_id)

    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    if request.method == 'POST':
        return community_event_creation(request, community_id)
    else:
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def community_event_creation(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/events

    Sends a request to the community server with the relevant data to create a new community
    """

    validations = ['title', 'description', 'location', 'datetime', 'duration', 'tags']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)
        
    client = CommunityEventClient()

    try:
        data = json.loads(request.body)

        req = community_event_pb2.EventDataRequest(
            community_id=community_id,
            title=data['title'],
            description=data['description'],
            location=data['location'],
            datetime=data['datetime'],
            duration=data['duration'],
            tags=data['tags'],
            lat_lng=data.get('lat_lng', None)
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception as e:  # Occurs if the JSON is valid but the data is not
        print(e)
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.CreateResponse = client.create(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        'event_id': response.event_id
    })


def community_event_view(request: WSGIRequest, community_id):
    """
    URL: localhost:8000/community/<int:community_id>/events

    Sends a request to the community server with the relevant data to create a new community
    """

    client = CommunityEventClient()

    try:
        req = community_event_pb2.ViewRequest(
            community_id=community_id,
            offset=int(request.GET.get('offset', '0')),
            limit=int(request.GET.get('limit', '1'))
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.ViewResponse = client.view(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    all_events = []

    if response.status.success:
        for event in response.event:
            json_event = MessageToDict(event)

            reformed_event = {
                    "id": json_event['id'],
                    "community_id": json_event['communityId'],
                    "title": json_event['title'],
                    "description": json_event['description'],
                    "location": json_event['location'],
                    "datetime": json_event['datetime'],
                    "duration": json_event['duration'],
                    "latitude": json_event.get('latitude', None),
                    "longitude": json_event.get('longitude', None),
                    "tags": json_event.get('tags', [])
                }

            all_events.append(reformed_event)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        "events": all_events
    })


def community_event_view_single(request: WSGIRequest, community_id, event_id):
    """
    Sends a request to the community server with the relevant data to fetch a community's data
    """
    client = CommunityEventClient()

    try:
        req = community_event_pb2.ViewOneRequest(
            event_id=event_id,
            community_id=community_id
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.ViewResponse = client.view_one(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    json_event = MessageToDict(response.event[0])

    longitude = json_event.get('longitude', None)
    latitude = json_event.get('latitude', None)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        'event': {
            'id': response.event[0].id,
            'community_id': response.event[0].community_id,
            'title': response.event[0].title,
            'description': response.event[0].description,
            'location': response.event[0].location,
            'datetime': response.event[0].datetime,
            'duration': response.event[0].duration,
            'latitude': latitude,
            'longitude': longitude
        }
    })


@csrf_exempt
def community_global_event_view(request: WSGIRequest):
    """
    URL: localhost:8000/community/events

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = CommunityEventClient()

    try:
        req = community_event_pb2.ViewGlobalRequest(
            offset=int(request.GET.get('offset', '0')),
            limit=int(request.GET.get('limit', '1'))
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.ViewResponse = client.view_global(req)
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    all_events = []

    if response.status.success:
        for event in response.event:
            json_event = MessageToDict(event)

            reformed_event = {
                    "id": json_event['id'],
                    "community_id": json_event['communityId'],
                    "title": json_event['title'],
                    "description": json_event['description'],
                    "location": json_event['location'],
                    "datetime": json_event['datetime'],
                    "duration": json_event['duration'],
                    "latitude": json_event.get('latitude', None),
                    "longitude": json_event.get('longitude', None),
                    "tags": json_event.get('tags', [])
                }

            all_events.append(reformed_event)

    return JsonResponse({
        'success': response.status.success,
        'http_status': response.status.http_status,
        'error_message': list(response.status.error_message),
        "global_events": all_events
    })


def community_event_edit(request: WSGIRequest, community_id, event_id):
    """
    Sends a request to the community server with the relevant data to update a community's data
    """

    validations = ['title', 'description', 'location', 'datetime', 'duration', 'tags']

    for validation in validations:
        if validation not in json.loads(request.body):
            return JsonResponse({'error': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)
        
    client = CommunityEventClient()

    try:
        data = json.loads(request.body)

        req = community_event_pb2.EditEventRequest(
            event_id=event_id,
            event_data=community_event_pb2.EventDataRequest(
                community_id=community_id,
                title=data['title'],
                description=data['description'],
                location=data['location'],
                datetime=data['datetime'],
                duration=data['duration'],
                tags=data['tags']
            )
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.EventResponse = client.update(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def community_event_delete(request: WSGIRequest, community_id, event_id):
    """
    Sends a request to the community server with the relevant data to delete a community event
    """

    client = CommunityEventClient()

    try:
        req = community_event_pb2.DeleteEventRequest(
            event_id=event_id,
            community_id=community_id
        )

    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 1'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        response: community_event_pb2.EventResponse = client.delete(req, request.COOKIES.get('sid'))
    except Exception:
        traceback.print_exc()
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred 2'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })
