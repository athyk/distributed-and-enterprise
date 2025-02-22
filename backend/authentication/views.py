from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignupForm, LoginForm

from django.http import HttpResponse
import json

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session["user_id"] = user.id  # Manual session login
            return HttpResponse(json.dumps({"message": "Signup successful", "user_id": user.id}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"errors": form.errors}), content_type="application/json", status=400)
    return render(request, "signup.html", {"form": SignupForm()})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            request.session["user_id"] = user.id  # Store user session
            return HttpResponse(json.dumps({"message": "Login successful", "user_id": user.id}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"errors": form.errors}), content_type="application/json", status=400)
    return render(request, "login.html", {"form": LoginForm()})
