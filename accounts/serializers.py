from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'password', 'is_verified']
    read_only_fields = ['is_verified']

class VerifyAcountSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  otp = serializers.CharField()

