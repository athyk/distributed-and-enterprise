import http
import json
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..common.middleware.auth import auth_required
from ..common.proto import chat_pb2_grpc, chat_pb2


@csrf_exempt
@auth_required(roles_required=['admin'], redirect_user=False)
def chat_message(request: WSGIRequest):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("chat-service:" + os.environ.get('CHAT_PORT', '50051'))
    stub = chat_pb2_grpc.ChatStub(channel)
    response: chat_pb2.MessageResponse = stub.SendMessage(chat_pb2.MessageRequest(message=data['message']))

    return JsonResponse({'message': response.message})
