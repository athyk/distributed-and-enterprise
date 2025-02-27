import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from backend.authentication.models import User

def home(request):
    return HttpResponse("Hello, world")

@csrf_exempt  # Remove in production!
def user_login(request):
    if request.method == "POST":
        print("request To create user made")
        try:
            data = json.loads(request.body.decode("utf-8"))
            print(f'Data Got: {data}')
            email = data.get("email")
            password = data.get("password")

            # Validation
            if not all([email, password]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Check if user exists
            user = User.objects.filter(email=email).first()
            if not user or not check_password(password, user.password):  # ✅ Use check_password for authentication
                if not user:
                    return JsonResponse({"error": "Invalid credentials (Not User)"}, status=400)

                elif not check_password(password, user.password):
                    return JsonResponse({"error": "Invalid credentials (Not Check Password)"}, status=400)

            return JsonResponse({"message": "Login successful"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # ❗ Remove this in production!
def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            password = data.get("password")
            password2 = data.get("password2")
            gender = data.get("gender")
            nickname = data.get("nickname")  

            # Validate required fields
            if not all([email, first_name, last_name, password, password2, gender]):
           
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

            # Create and save the user
            User.objects.create(
                email=email,
                password=make_password(password),  # ✅ Ensure password is hashed
                first_name=first_name,
                last_name=last_name,
                nickname=nickname,
                gender=gender,
            )

            return JsonResponse({"message": "User created successfully."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)