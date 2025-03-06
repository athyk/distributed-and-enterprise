import http
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from google.protobuf import empty_pb2

from backend.common.proto import data_fetching_pb2, data_fetching_pb2_grpc


@csrf_exempt
def get_tags(request: WSGIRequest):
    """
    Sends a request to the authentication server with the relevant data to register a new user.
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = data_fetching_pb2_grpc.DataFetchStub(channel)
    response: data_fetching_pb2.DataListResponse = stub.FetchTags(empty_pb2.Empty())

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'data': list(response.data)
    })


@csrf_exempt
def get_degrees(request: WSGIRequest):
    """
    Sends a request to the authorisation server with the relevant data to log in to an account
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = data_fetching_pb2_grpc.DataFetchStub(channel)
    response: data_fetching_pb2.DataListResponse = stub.FetchDegrees(empty_pb2.Empty())

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'data': list(response.data)
    })
