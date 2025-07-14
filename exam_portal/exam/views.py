from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, OTPForm
from .models import CustomUser
import random
from django.contrib.auth.decorators import login_required

# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # ... validate inputs ...

        if CustomUser.objects.filter(username=username).exists():
            error = "Username already exists!"
            return render(request, 'exam/register.html', {'error': error})

        otp_code = str(random.randint(100000, 999999))  # generate OTP
        user = CustomUser.objects.create_user(username=username, password=password)
        user.is_verified = False
        user.otp = otp_code
        user.save()

        # TODO: send OTP via email or SMS here. For now, show it on screen
        return render(request, 'exaam/otp.html', {'username': username, 'otp': otp_code})

    return render(request, 'exam/register.html')

# OTP Verification View
def otp_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        entered_otp = request.POST.get('otp')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            error = "User not found!"
            return render(request, 'exam/otp.html', {'error': error})

        if user.otp == entered_otp:
            user.is_verified = True
            user.otp = None
            user.save()
            return redirect('login')
        else:
            error = "Invalid OTP! Please try again."
            return render(request, 'exam/otp.html', {'error': error, 'username': username})

    # For GET requests, show a form to enter OTP
    return render(request, 'exam/otp.html')


# Login View
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('exam/dashboard')
            else:
                error = "Account not verified! Please verify via OTP."
        else:
            error = "Invalid username or password."

    return render(request, 'exam/login.html', {'error': error})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    context = {
        'username': user.username,
        'is_student': user.is_student,
        'is_superuser': user.is_superuser,
        'is_verified': user.is_verified,
    }
    return render(request, 'dashboard.html', context)
