import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import SignupForm, LoginForm
from .models import User

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                request.session["user_id"] = user.id  # Manual session login
                return HttpResponse(json.dumps({"message": "Signup successful", "user_id": user.id}), content_type="application/json")
            except Exception as e:
                return HttpResponse(json.dumps({"error": str(e)}), content_type="application/json", status=400)
        else:
            return HttpResponse(json.dumps({"errors": form.errors}), content_type="application/json", status=400)
    return render(request, "signup.html", {"form": SignupForm()})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)  # Check if user exists
                user = authenticate(request, email=email, password=password)  # Authenticate user
                if user:
                    request.session["user_id"] = user.id  # Store user session
                    return HttpResponse(json.dumps({"message": "Login successful", "user_id": user.id}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"error": "Invalid password"}), content_type="application/json", status=400)
            except User.DoesNotExist:
                return HttpResponse(json.dumps({"error": "User with this email does not exist"}), content_type="application/json", status=400)
        else:
            return HttpResponse(json.dumps({"errors": form.errors}), content_type="application/json", status=400)
    return render(request, "login.html", {"form": LoginForm()})
