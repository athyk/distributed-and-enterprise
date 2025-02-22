from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.authentication"  # ✅ Match this with `INSTALLED_APPS`
