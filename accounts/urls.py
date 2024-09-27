from django.urls import path
from .views import RegisterAPI, VerifyOTP, all_users, resend_otp

urlpatterns = [
  path('register/', RegisterAPI.as_view(), name='register'),
  path('verify/', VerifyOTP.as_view(), name='verify'),
  path('all_users/', all_users, name='all-users'),
  path('resend_otp/<int:id>/', resend_otp, name='resend-otp'),
]

