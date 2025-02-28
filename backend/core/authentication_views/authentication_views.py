import http
import json
import os

import grpc
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto import authentication_pb2, authentication_pb2_grpc


def register_user(request: WSGIRequest):
    """
    Sends a request to the community server with the relevant data to delete a community
    """

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

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message),
        'user_id': response.user_id
    })


def login_user(request: WSGIRequest):
    """
    Sends a request to the authorisation server with the relevant data to log in to an account
    """

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.AuthenticationResponse = stub.LoginUser(authentication_pb2.LoginRequest(
        email=data['email'],
        password=data['password']
    ))

    return JsonResponse({
        'success': response.success,
        'http_status': response.http_status,
        'error_message': list(response.error_message)
    })


def send_email_verification_code(request: WSGIRequest):
    """
    Sends a request to the authorisation server to send an email to the user to verify account
    """

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


def verify_email_and_account(request: WSGIRequest):
    """
    Sends a request to the authorisation server to verify the account
    """

    data = json.loads(request.body)

    channel = grpc.insecure_channel("auth-service:" + os.environ.get('AUTHENTICATION_PORT', '50053'))
    stub = authentication_pb2_grpc.AuthenticationStub(channel)
    response: authentication_pb2.EmailVerifiedResponse = stub.EmailConfirmationRequest(authentication_pb2.EmailAuthVerify(
        email=data['email'],
        otp=otp,
        id=data['id']
    ))

    return JsonResponse({
        'verified': response.verified,
        'error_message': list(response.error_message)
    })
