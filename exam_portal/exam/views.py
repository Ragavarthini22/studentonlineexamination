from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import get_user_model

@login_required
def dashboard_view(request):
    return render(request, "exam/dashboard.html", {"user": request.user})

def generate_otp():
    return str(random.randint(100000, 999999))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
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
            return redirect("dashboard")

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

@csrf_protect
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    
def home_view(request):
    return render(request, 'exam/home.html')

User = get_user_model()  # In case you're using CustomUser

def authenticate_user_type(request, expected_type):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user and hasattr(user, 'user_type') and user.user_type == expected_type:
        login(request, user)
        return user
    else:
        messages.error(request, "Invalid credentials or role.")
        return None

def student_login_view(request):
    if request.method == "POST":
        user = authenticate_user_type(request, 'student')
        if user:
            return redirect("student_dashboard")
    return redirect("homepage")

def teacher_login_view(request):
    if request.method == "POST":
        user = authenticate_user_type(request, 'teacher')
        if user:
            return redirect("teacher_dashboard")
    return redirect("homepage")

def admin_login_view(request):
    if request.method == "POST":
        user = authenticate_user_type(request, 'admin')
        if user:
            return redirect("admin_dashboard")
    return redirect("homepage")

def student_register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        user_type = request.POST.get("user_type")  # Expected values: 'student', 'teacher', 'admin'

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("homepage")

        if not user_type or user_type not in ["student", "teacher", "admin"]:
            messages.error(request, "Please select a valid user type.")
            return redirect("homepage")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("homepage")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("homepage")

        # Create user but set inactive until OTP verified
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.user_type = user_type  # Custom field on your CustomUser model
        user.save()

        # Generate and send OTP
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["user_to_verify"] = username

        send_mail(
            "Your OTP Verification Code",
            f"Here is your OTP: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("otp")

    return redirect("homepage")

def teacher_register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        user_type = request.POST.get("user_type")  # Expected values: 'student', 'teacher', 'admin'

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("homepage")

        if not user_type or user_type not in ["student", "teacher", "admin"]:
            messages.error(request, "Please select a valid user type.")
            return redirect("homepage")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("homepage")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("homepage")

        # Create user but set inactive until OTP verified
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.user_type = user_type  # Custom field on your CustomUser model
        user.save()

        # Generate and send OTP
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["user_to_verify"] = username

        send_mail(
            "Your OTP Verification Code",
            f"Here is your OTP: {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("otp")

    return redirect("homepage")
