from django.shortcuts import render
from django.contrib.login import authenticate, login
from django.contrib.login.decorates import login_required
from django.contrib import messages 


# Create your views here.
#def home(request):
     #return render (request,'exam/login.html')
     #return render (request,'exam/register.html')
     #return render (request,'exam/otp.html')
def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect('login')
return render (request, 'exam/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password.")
            return.redirect('login')
    return render(request, 'exam/login.html')

def verify_otp(request):
    messages.info(request, "OTP verification placeholder.")
    return redirect('admin list')
