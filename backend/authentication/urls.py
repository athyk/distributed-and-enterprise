from django.urls import path
from . import views
from . import verify

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.create_user, name="signup"),  # Change to `signup`
    path("send/", verify.send_verifcation_code, name="send"),
    path("verify/", verify.verify_otp, name="verify"),
]
