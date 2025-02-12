from datetime import datetime, UTC

from django.views.decorators.cache import cache_page
from django.http import JsonResponse


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
