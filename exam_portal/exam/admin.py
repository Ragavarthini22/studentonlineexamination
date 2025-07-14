from django.contrib import admin
from .models import Questions
from .models import CustomUser, Exam, StudentAnswer, Result
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Questions)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Exam)
admin.site.register(StudentAnswer) 
admin.site.register(Result)