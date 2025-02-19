from django.http import JsonResponse
from your_app.models import User
from django.utils.timezone import now

from django.shortcuts import render, redirect
from your_app.forms import UserForm

def create_user(request):


    if request.method == "POST":
        form = UserForm(request.POST)  # Bind form data from the request
        if form.is_valid():  # Validate the form
             # Validation passed!

             first_name = form.cleaned_data["first_name"]
        



            user = form.save()  # Save the form data to the database
            return redirect("success_page")  # Redirect to a success page
    else:
        form = UserForm()

    return render(request, "create_user.html", {"form": form})




