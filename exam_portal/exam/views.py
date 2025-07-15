from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegisterForm
import random

User = get_user_model()  # ✅ Fix: get custom user model

# Store OTPs temporarily (in memory)
otp_store = {}


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            otp = str(random.randint(100000, 999999))
            otp_store[username] = otp
            request.session["otp_user"] = username
            print(f"OTP for {username}: {otp}")
            messages.info(request, "OTP sent. Check terminal.")
            return redirect('auth_page')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('auth_page')
    return redirect('auth_page')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('auth_page')
    else:
        form = RegisterForm()
    return render(request, 'exam/auth.html', {"form": form, "show": "register-form"})


def verify_otp(request):
    username = request.session.get("otp_user")
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        actual_otp = otp_store.get(username)
        if entered_otp == actual_otp:
            user = User.objects.get(username=username)  # ✅ Now works
            login(request, user)
            del request.session["otp_user"]
            messages.success(request, "OTP verified. You are now logged in.")
            return redirect('auth_page')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('auth_page')
    return render(request, 'exam/auth.html', {"show": "otp-form"})


def auth_page(request):
    form = RegisterForm()
    return render(request, "exam/auth.html", {"form": form, "show": "login-form"})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('auth_page')