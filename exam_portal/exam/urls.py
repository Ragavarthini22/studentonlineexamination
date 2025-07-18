"""
URL configuration for exam_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
   # path('register/', views.register_view, name='register'),
   #path('otp/', views.otp_view, name='otp'),
   # path('resend-otp/', views.resend_otp, name='resend_otp'),
   #path('login/', views.login_view, name='login'),  # ✅ Ensure this is here
    #path('dashboard/', views.dashboard_view, name='dashboard'),
    #path('success/', views.auth_success, name='auth_success'),
    #path('logout/', views.logout_view, name='logout'),
    path('home/',views.home_view, name='home'),
   

    # Role-Based Login Handlers
    path('login/student/', views.student_login_view, name='student_login'),
    path('login/teacher/', views.teacher_login_view, name='teacher_login'),
    path('login/admin/', views.admin_login_view, name='admin_login'),
    path('register/student/', views.student_register_view, name='student_login'),
    path('register/teacher/', views.teacher_register_view, name='teacher_login'),
    path('register/admin/', views.admin_register_view, name='admin_login'),

    # Role Dashboards
    path('dashboard/student/', views.student_login_view, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_login_view, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_login_view, name='admin_dashboard'),
]

