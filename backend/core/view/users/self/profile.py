import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.files import StorageClient
from backend.common.middleware.auth import auth_required
from backend.common.proto.accounts_pb2 import UpdateRequest, Response
from backend.common.services import AccountsClient


@auth_required()
@csrf_exempt
def update_profile_picture(request: WSGIRequest):
    """
    Update the user's own account profile picture
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    client = AccountsClient()
    real_user: dict | None = client.check_session(request.COOKIES.get('sid'))

    if not real_user:
        return JsonResponse({'success': False, 'error_message': 'Invalid Session'}, status=http.HTTPStatus.UNAUTHORIZED)

    try:
        if not request.FILES.get("file"):
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file = request.FILES["file"]
        minio_client = StorageClient()

        file_url = minio_client.compress_and_upload_image(file)
        print(file_url)

        if not file_url:
            return JsonResponse({"success": False, "error_message": "Failed to upload file"}, status=500)

        data = {
            "id": real_user["id"],
            "picture_url": file_url,
        }
        req = UpdateRequest(
            user=data,
            is_self=True
        )
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)

    try:
        res: Response = client.update(req)
    except Exception as e:
        print(e)  # this prevents showing sensitive information to the user
        return JsonResponse({'success': False, 'error_message': 'An Unknown Error Occurred'},
                            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    http_res = {
        'success': res.success,
    }

    if len(res.error_message) > 0:
        http_res['error_message'] = list(res.error_message)

    return JsonResponse(http_res, status=res.http_status)
