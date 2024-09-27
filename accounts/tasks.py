

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User
import random

@shared_task
def send_otp_via_mail(email):
  print("Task Started")
  subject = "Your verification email."
  otp = random.randint(1000, 9999)
  message = f"Your verification otp is {otp}, Expires in 5min."
  email_from = settings.EMAIL_HOST_USER
  try:
    send_mail(subject, message, email_from, [email])

    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()
    print(f"Email sent successfully to : {email}")
  except Exception as e:
    print(f"Failed ton send OTP to : {email}")


@shared_task
def otp_timer(email):
  try:
    user = User.objects.get(email=email)
    user.otp = None
    print("OTP expired!")
    user.save()
  except User.DoesNotExist:
    pass
  