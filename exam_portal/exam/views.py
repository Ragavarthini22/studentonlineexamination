from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from exam import views

# Home page (public)
def home(request):
    return render(request, 'exam/home.html')

# Student login/register page
def student_login(request):
    return render(request, 'exam/student_login.html')

# Teacher login/register page
def teacher_login(request):
    return render(request, 'exam/teacher_login.html')

# STUDENT login form handler
def student_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid student credentials.")
            return redirect('student_login')

    return redirect('student_login')

# STUDENT register form handler
def student_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_photo = request.FILES.get('profile_photo')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('student_login')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('student_login')

        user = User.objects.create_user(username=username, email=email, password=password1)
        # Save profile_photo if using extended user profile model

        login(request, user)
        return redirect('student_dashboard')

    return redirect('student_login')

# TEACHER login form handler
def teacher_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Invalid teacher credentials.")
            return redirect('teacher_login')

    return redirect('teacher_login')

# TEACHER register form handler
def teacher_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_photo = request.FILES.get('profile_photo')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('teacher_login')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('teacher_login')

        user = User.objects.create_user(username=username, email=email, password=password1)
        # Save profile_photo if using extended user profile model

        login(request, user)
        return redirect('teacher_dashboard')

    return redirect('teacher_login')

# Logout view (shared)
def logout_view(request):
    logout(request)
    return redirect('home')


def about_view(request):
    return render(request, 'exam/about.html')