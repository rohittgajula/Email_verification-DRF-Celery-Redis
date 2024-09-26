from django.urls import path
from .views import RegisterAPI, VerifyOTP

urlpatterns = [
  path('register/', RegisterAPI.as_view(), name='register'),
  path('verify/', VerifyOTP.as_view(), name='verify'),
]