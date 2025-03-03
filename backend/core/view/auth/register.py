import http
import json
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto.auth_pb2 import *
from backend.common.services import AuthClient


@csrf_exempt
def register_user(request: WSGIRequest):
    """
    Creates a user account
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error_message': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AuthClient()

    try:
        data = json.loads(request.body)

        if 'skip_email' not in json.loads(request.body):
            data['skip_email'] = False

        req = RegistrationRequest(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=data['dob'],
            gender=data['gender'],
            degree=data['degree'],
            year_of_study=data['year_of_study'],
            grad_date=data['grad_date'],
            tags=data['tags']
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception as e:  # Occurs if the JSON is valid but the data is not
        # While if statements are used elsewhere, a loop is better since there is more of them
        data = json.loads(request.body)

        validations = ['email', 'password', 'first_name', 'last_name', 'dob', 'gender', 'degree', 'year_of_study',
                       'grad_date', 'tags']

        for validation in validations:
            if validation not in data:
                return JsonResponse({'success': False, 'error_message': f'Key: {validation} Not Found'}, status=http.HTTPStatus.BAD_REQUEST)

        print(e)
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: LoginResponse = client.register_user(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
        'user_id': res.user_id
    }

    if len(res.error_message) > 0:
        print(res.error_message)
        http_res['error_message'] = list(res.error_message)

    # user is always filled out, even if the user is not created.
    # so check id, as it's the only required field.
    if res.user.id != "":
        http_res['user'] = client.user_to_json(res.user)

    if res.otp_required:
        http_res['otp_required'] = res.otp_required

    return JsonResponse(http_res, status=res.http_status)

