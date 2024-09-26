from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .manager import UserManager


class User(AbstractUser):
  username = models.CharField(max_length=150, null=True, blank=True)
  email = models.EmailField(max_length=150, unique=True)
  is_verified = models.BooleanField(default=False)
  otp = models.CharField(max_length=6, null=True, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()

  def __str__(self):
    return self.email
  

