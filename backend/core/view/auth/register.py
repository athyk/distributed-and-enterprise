import http
import json
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.proto.accounts_pb2 import RegistrationRequest, LoginResponse
from backend.common.services import AccountsClient


@csrf_exempt
def register_user(request: WSGIRequest):
    """
    Creates a user account
    """

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error_message': 'HTTP Method Invalid'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    if not request.body:
        return JsonResponse({'success': False, 'error_message': 'No Data Provided'}, status=http.HTTPStatus.BAD_REQUEST)

    client = AccountsClient()

    try:
        data = json.loads(request.body)

        if 'skip_email' not in data:
            data['skip_email'] = False

        req = RegistrationRequest(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['dob'],
            gender=data['gender'],
            degree_id=data['degree_id'],
            year_of_study=data['year_of_study'],
            grad_date=data['grad_date'],
            tags=data['tags'],
            skip_email=data['skip_email'],
            # Do not fill in rank, it's defaulted to 'user' in the service
        )

    except json.JSONDecodeError:  # Occurs if the JSON is invalid
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)
    except Exception:  # Occurs if the JSON is valid but the data is not
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'}, status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        res: LoginResponse = client.register(req)
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

    # user is filled out but left empty, even if the user is not created.
    # so check id, as it's the only required field.
    if res.user.id != 0:
        http_res['user'] = client.user_to_json(res.user)

    if res.otp_required:
        http_res['otp_required'] = res.otp_required
        client.save_otp(res.user_id, res.email_id)

    # DO NOT set session here as the user's email has not been verified, send them over to login.

    return JsonResponse(http_res, status=res.http_status)
