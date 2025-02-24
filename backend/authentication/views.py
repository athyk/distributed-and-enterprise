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
from jsonschema import ValidationError



def home(request):
    return HttpResponse("Hello, world")


@csrf_exempt  # Remove this in production!
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data.get("email")
            password = data.get("password")

            # Validation
            if not all([email, password]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Check if user exists
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if user is None:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

            return JsonResponse({"message": "Login successful"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt  # Remove in production!
def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            full_name = f"{first_name} {last_name}"
            password = data.get("password")
            password2 = data.get("password2")
            gender = data.get("gender")
            nickname = data.get("nickname")

            # Validate required fields
            if not all([email, first_name, last_name, password, password2, gender, nickname]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Validate password match
            if password != password2:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            # Validate email uniqueness
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with this email already exists"}, status=400)

            # Validate gender choice
            if gender not in dict(User.GENDER_CHOICES):
                return JsonResponse({"error": "Invalid gender selection"}, status=400)

            # Create the user (password is automatically hashed)
            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                nickname=nickname,
                gender=gender,  
            )

            return JsonResponse({"message": "User created successfully. Please verify your email."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
