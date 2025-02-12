# Caching

Caching relies on [`django_redis`](https://github.com/jazzband/django-redis)

## Example usage

Ensure docker is installed on your machine. To test the caching in a django project, follow the steps below:

- Go into an app (e.g. `core`)
- Add the following code to a view:
```python
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
```

- Add the following to your `urls.py`:

Do note: some of this code may already be present in the `urls.py` file
```python
from django.urls import path
from .views import ping1, ping5, ping10

urlpatterns = [
    path('ping/', ping1),
    path('ping/1/', ping1),
    path('ping/5/', ping5),
    path('ping/10/', ping10),
]
```

- Add the following code to the `urls.py` located in `unihub_project`:

Do note: some of this code may already be present in the `urls.py` file, so you may need to add the `include` import and the `path` line.
And just the `path` line if `urlpatterns` is already present.
```python
from django.urls import path, include

urlpatterns = [
    path('', include("core.urls")),
]
```

- Run `docker-compose up --build`.
- Visit http://localhost:8000/ping/1/ in your browser for a 1-second cache.
- Visit http://localhost:8000/ping/5/ in your browser for a 5-second cache.
- Visit http://localhost:8000/ping/10/ in your browser for a 10-second cache.

As you may see in the response, you will get `{"message": "pong", "cached_at": "11:28:47:739864"}`

The `cached_at` field will change every time the cache is refreshed, it's more visible in a 10-second cache.

## Raw Redis/Storing normal data


Access Redis directly using the following code:
```python
from django_redis import get_redis_connection

redis_conn = get_redis_connection("default") # Use "default" as that's what is present in the settings.py
redis_conn.set('key', 'val') # setting the key-value pair
val = redis_conn.get('key') # getting the value from the key
```

or 

Access django implementation of redis (Still using redis but easier to use) using the following code:
```python
from django.core.cache import cache
cache.set('key', 'val', timeout=10)  # Cache for 10 seconds

value = cache.get('key') # Output: 'val'
cache.delete('key') # Delete the key and value
```

For more information see a medium article [here](https://medium.com/django-unleashed/caching-in-django-with-redis-a-step-by-step-guide-40e116cb4540)