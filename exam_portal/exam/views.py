from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
import random


# 🔀 Entry point: switches between login/register/otp using ?show=
def auth_page(request):
    show = request.GET.get('show', 'login')
    return render(request, 'exam/auth.html', {'show': show})


# 📝 Register a user and send OTP
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'exam/auth.html', {
                'show': 'register',
                'error': 'Username already exists!'
            })

        # Create user and generate OTP
        otp_code = str(random.randint(100000, 999999))
        user = CustomUser.objects.create_user(username=username, password=password)
        user.is_verified = False
        user.otp = otp_code
        user.save()

        # Render OTP form with OTP shown (dev purpose)
        return render(request, 'exam/auth.html', {
            'show': 'otp',
            'username': username,
            'otp': otp_code  # In production, you'd email or SMS this
        })

    return redirect('/auth/?show=register')


# 🔐 Verify OTP
def otp_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        entered_otp = request.POST.get('otp')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return render(request, 'exam/auth.html', {
                'show': 'otp',
                'error': 'User not found!',
                'username': username
            })

        if user.otp == entered_otp:
            user.is_verified = True
            user.otp = None
            user.save()
            return redirect('/auth/?show=login')
        else:
            return render(request, 'exam/auth.html', {
                'show': 'otp',
                'username': username,
                'error': 'Invalid OTP!'
            })

    return redirect('/auth/?show=otp')


# 🔓 Login after verification
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'exam/auth.html', {
                    'show': 'login',
                    'error': 'Please verify your account using OTP.'
                })
        else:
            return render(request, 'exam/auth.html', {
                'show': 'login',
                'error': 'Invalid username or password.'
            })

    return redirect('/auth/?show=login')


# 🧾 Dashboard
@login_required(login_url='/auth/?show=login')
def dashboard_view(request):
    user = request.user
    return render(request, 'exam/dashboard.html', {
        'username': user.username,
        'is_student': user.is_student,
        'is_superuser': user.is_superuser,
        'is_verified': user.is_verified,
    })


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('/auth/?show=login')