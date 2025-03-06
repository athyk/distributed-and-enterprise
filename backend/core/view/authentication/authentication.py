import http
import json
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import authentication_pb2, authentication_pb2_grpc


@csrf_exempt
def register_user(request: WSGIRequest):
    """
    Sends a request to the authentication server with the relevant data to register a new user.
    """

    try:
        print(request.session["user_id"])
    except:
        pass

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.AuthenticationResponse = stub.RegisterUser(authentication_pb2.RegistrationRequest(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=data['dob'],
        gender=data['gender'],
        degree=data['degree'],
        year_of_study=data['year_of_study'],
        grad_year=data['grad_year'],
        tag=data['tag']
    ))

    request.session["user_id"] = response.user_id

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'user_id': response.user_id
    })


@csrf_exempt
def login_user(request: WSGIRequest):
    """
    Sends a request to the authorisation server with the relevant data to log in to an account
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.AuthenticationResponse = stub.LoginUser(authentication_pb2.LoginRequest(
        email=data['email'],
        password=data['password']
    ))

    request.session["user_id"] = response.user_id

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


@csrf_exempt
def send_email_verification_code(request: WSGIRequest):
    """
    Sends a request to the authorisation server to send an email to the user to verify account
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.EmailAuthSent = stub.SendEmailRequest(authentication_pb2.EmailAuthRequest(
        email=data['email'],
        skip=data['skip']
    ))

    return JsonResponse({
        'sent': response.sent,
        'error_message': list(response.error_message)
    })


@csrf_exempt
def verify_email_and_account(request: WSGIRequest):
    """
    Sends a request to the authorisation server to verify the account
    """

    if request.method != 'POST':
        return JsonResponse({'error': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
    if not request.body:
        return JsonResponse({'error': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.EmailVerifiedResponse = stub.EmailConfirmationRequest(authentication_pb2.EmailAuthVerify(
        email=data['email'],
        otp=data['otp'],
        id=data['id']
    ))

    return JsonResponse({
        'verified': response.verified,
        'error_message': list(response.error_message)
    })
