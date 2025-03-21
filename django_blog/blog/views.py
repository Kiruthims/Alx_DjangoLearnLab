from django.shortcuts import render, redirect # to render templates for various views and also redrct after success
from.forms import CustomUserCreationForm # required for user registr
from django.contrib.auth.decorators import login_required #to protect a view from unauthenticated usrs
from django.contirb.auth import login #to login users after regstn
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserUpdateForm 


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logs in the user after regstrn
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("home")  # Redirect to home
        else:
            messages.error(request, "There was an error with your registration. Please try again.")    
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  #reloading
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form})
