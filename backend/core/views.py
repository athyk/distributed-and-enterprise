import http
import json
import os
from datetime import datetime, UTC

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..common.proto import chat_pb2_grpc, chat_pb2

@cache_page(10)  # cache for 10 seconds
def ping10(request):
    print("ping10, cache miss/refresh")
    time_now = datetime.now(UTC).strftime('%H:%M:%S:%f')
    return JsonResponse({'message': 'pong', 'cached_at': time_now})


@cache_page(5)  # cache for 5 seconds
def ping5(request):
    print("ping5, cache miss/refresh")
    time_now = datetime.now(UTC).strftime('%H:%M:%S:%f')
    return JsonResponse({'message': 'pong', 'cached_at': time_now})


@cache_page(1)  # cache for 1 second
def ping1(request):
    print("ping1, cache miss/refresh")
    time_now = datetime.now(UTC).strftime('%H:%M:%S:%f')
    return JsonResponse({'message': 'pong', 'cached_at': time_now})


@csrf_exempt
def chat_message(request: WSGIRequest):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("chat-service:" + os.environ.get('CHAT_PORT', '50051'))
    stub = chat_pb2_grpc.ChatStub(channel)
    response: chat_pb2.MessageResponse = stub.SendMessage(chat_pb2.MessageRequest(message=data['message']))

    return JsonResponse({'message': response.message})