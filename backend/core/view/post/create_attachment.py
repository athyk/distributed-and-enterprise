import http

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from backend.common.files import StorageClient
from backend.common.middleware.auth import auth_required


@auth_required()
@csrf_exempt
def create_attachment(request: WSGIRequest):
    """
    Creates a post attachment
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    try:
        if not request.FILES.get("file"):
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file = request.FILES["file"]
        minio_client = StorageClient()

        file_url = minio_client.compress_and_upload_image(file)
        print(file_url)

        if not file_url:
            return JsonResponse({"success": False, "error_message": "Failed to upload file"}, status=500)

        return JsonResponse({"success": True, "file_url": file_url})
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error_message': 'Invalid JSON'}, status=http.HTTPStatus.BAD_REQUEST)