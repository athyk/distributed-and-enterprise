import http
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import data_fetching_pb2_grpc, data_fetching_pb2
from google.protobuf import empty_pb2


@csrf_exempt
def fetch_degrees(request: WSGIRequest):
    """
    URL: localhost:8000/degrees

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTH_PORT', '50053'))
    stub = data_fetching_pb2_grpc.DataFetchStub(channel)
    response: data_fetching_pb2.DataListResponse = stub.FetchDegrees(empty_pb2.Empty())

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'data': list(response.data)
    })


@csrf_exempt
def fetch_tags(request: WSGIRequest):
    """
    URL: localhost:8000/tags

    Sends a request to the community server with the relevant data to create a new community
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTH_PORT', '50053'))
    stub = data_fetching_pb2_grpc.DataFetchStub(channel)
    response: data_fetching_pb2.DataListResponse = stub.FetchTags(empty_pb2.Empty())

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'data': list(response.data)
    })
