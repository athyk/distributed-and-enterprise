from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm  # Assuming you have a form named UserRegistrationForm

from django.contrib.auth.hashers import make_password




def create_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.password(make_password(form.cleaned_data["password"]))
                user.save()

                messages.success(request, "Account created successfully!")
                return redirect("success_page")
            except IntegrityError:  # Handles duplicate email, etc.
                messages.error(request, "A user with this email already exists.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    # If form is invalid or insertion fails, re-render the form with errors
    return render(request, "create_user.html", {"form": form})


