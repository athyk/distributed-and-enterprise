from backend.common.utils import verify_string, verify_boolean, verify_list, verify_integer
from backend.community.database.database import get_db
from werkzeug.security import check_password_hash

from backend.auth.database.models import User


def register_user(email: str, password: str) -> tuple[bool, int, list]:


















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