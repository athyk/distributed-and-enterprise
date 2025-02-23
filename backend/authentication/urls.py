from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.create_user, name="signup"),  # Change to `signup`
]
