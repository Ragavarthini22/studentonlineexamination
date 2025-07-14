from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentAnswer

# ✅ Registration form for Student
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

# ✅ Form for answering questions (optional for individual answers)
class AnswerForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ['selected_option']


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)