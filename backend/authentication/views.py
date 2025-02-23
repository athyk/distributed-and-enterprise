import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt



def home(request):
    return HttpResponse("Hello, world")

def user_login(request):  # Renamed from 'login' to 'user_login'
    return HttpResponse("Login page")

@csrf_exempt  # Disable CSRF for testing (remove in production)
def create_user(request):
    if request.method == "POST":
        try:
            # Check if request body exists
            if not request.body:
                return JsonResponse({"error": "Request body is empty"}, status=400)

            data = json.loads(request.body.decode("utf-8"))  # Parse JSON data

            email = data.get("email")
            first_name = data.get("firstname")
            last_name = data.get("lastname")
            password = data.get("password")
            password2 = data.get("password2")
            nickname = data.get("nickname")
            gender = data.get("gender")

            # Validate required fields
            if not all([email, first_name, last_name, password, password2, nickname, gender]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Check if passwords match
            if password != password2:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with this email already exists"}, status=400)

            # Create user but do not activate yet
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                is_active=False  # Deactivate until email is verified
            )

            return JsonResponse({"message": "User created successfully. Please verify your email."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)