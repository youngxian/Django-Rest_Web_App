"""justeece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from accounts.views import SignupView, LoginView, DashboardView, ProfileView, VerificationView, LogoutView,\
UserListView, EmailVerificationConfirmationLinkView, ResendVerificationToken

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm/<token>/<id>',
        VerificationView.as_view(), name='email_confirmation'),    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_list/<data>', UserListView.as_view(), name='profile'),
    path('email-verification-confirmation/', EmailVerificationConfirmationLinkView.as_view(), 
        name="email_verification_confirmation"),
    path('resendverification/<email>',
        ResendVerificationToken.as_view(), name='resendverification'),
]
