from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import CustomUser, Exam, Questions, StudentAnswer, Result
from .forms import StudentRegisterForm, AnswerForm
import random

# Create your views here.
#def home(request):
     #return render (request,'exam/login.html')
     #return render (request,'exam/register.html')
     #return render (request,'exam/otp.html')

def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Register Student
def register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.otp = generate_otp()
            user.save()
            request.session['user_id'] = user.id
            return redirect('otp')
    else:
        form = StudentRegisterForm()
    return render(request, 'exam/register.html', {'form': form})

# ✅ OTP Verification
def otp_verification(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        input_otp = request.POST['otp']
        if input_otp == user.otp:
            user.is_active = True
            user.is_verified = True
            user.otp = ''
            user.save()
            return redirect('login')
    return render(request, 'exam/otp.html')

# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_verified:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'exam/login.html')

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ Student Dashboard: List of Exams
@login_required
def dashboard(request):
    if not request.user.is_student:
        return HttpResponseForbidden("Only students allowed.")
    exams = Exam.objects.all()
    return render(request, 'exam/dashboard.html', {'exams': exams})

# ✅ Take Exam (Display Questions)
@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.id))
            StudentAnswer.objects.create(
                student=request.user,
                question=q,
                selected_option=selected
            )
            if selected == q.answer:
                score += 1

        Result.objects.create(
            student=request.user,
            exam=exam,
            score=score
        )
        return redirect('result', exam_id=exam.id)

    return render(request, 'exam/take_exam.html', {'exam': exam, 'questions': questions})

# ✅ View Result
@login_required
def result_view(request, exam_id):
    result = get_object_or_404(Result, student=request.user, exam_id=exam_id)
    return render(request, 'exam/result.html', {'result': result})
