from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
import ssl
import certifi 

# Monkey patch: Force SSL context to use certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


def generate_otp():
    return str(random.randint(100000, 999999))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("auth_success")
    return render(request, "exam/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]

        if password != confirm:
            return render(request, "exam/register.html", {"error": "Passwords do not match"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        otp = generate_otp()
        request.session["otp"] = otp
        request.session["user_to_verify"] = username

        send_mail(
            "Your OTP",
            f"Here is your OTP: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        return redirect("otp")

    return render(request, "exam/register.html")

def otp_view(request):
    if request.method == "POST":
        entered = "".join([request.POST.get(f"digit{i}") for i in range(1, 7)])
        session_otp = request.session.get("otp")
        username = request.session.get("user_to_verify")

        if entered == session_otp and username:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("auth_success")

    return render(request, "exam/otp.html")

def resend_otp(request):
    username = request.session.get("user_to_verify")
    if username:
        user = User.objects.get(username=username)
        otp = generate_otp()
        request.session["otp"] = otp
        send_mail(
            "Your New OTP",
            f"Your new OTP is: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    return redirect("otp")

def auth_success(request):
    return render(request, "exam/auth_success.html")

def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("login")
    
@login_required
def dashboard_view(request):
    return render(request, "exam/dashboard.html", {"user": request.user})