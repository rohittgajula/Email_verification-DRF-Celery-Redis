from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, VerifyAcountSerializer
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth.hashers import make_password
from .tasks import send_otp_via_mail, otp_timer

class RegisterAPI(APIView):
  def post(self, request):
    try:
      data = request.data
      serializer = UserSerializer(data=data)
      if serializer.is_valid():
        password = make_password(data['password'])
        serializer.save(password = password)
        send_otp_via_mail.delay(serializer.data['email'])
        otp_timer.apply_async((serializer.data['email'],), countdown=600)
        return Response({
          'status':200,
          'message':'Registration successful, check your email for OTP verification, Expires in 5min.',
          'data':serializer.data,
        }, status.HTTP_200_OK)
      return Response({
        'status':400,
        'message':'Something went wrong.',
        'data':serializer.errors
      }, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({
        'status':500,
        'message':'error occured during registration',
        'error':str(e)
      }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTP(APIView):
  def post(self, request):
    try:
      data = request.data
      serializer = VerifyAcountSerializer(data=data)

      if serializer.is_valid():
        email = serializer.data['email']
        otp = serializer.data['otp']

        user = User.objects.filter(email = email)
        if not user.exists():
          return Response({
            'status': 404,
            'message':"Invalid email"
          }, status.HTTP_404_NOT_FOUND)
        
        if user[0].otp != otp:
          return Response({
            'status':400,
            'message':"Wrong otp."
          }, status.HTTP_400_BAD_REQUEST)
        else:
          user = user.first()
          user.is_verified = True
          user.save()
          return Response({
            'status':202,
            'message':"Account verified."
          }, status.HTTP_202_ACCEPTED)

    except Exception as e:
      return Response({
        'status':400,
        'message':'Error occured while verifying.',
        'error':str(e)
      }, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def resend_otp(request, id):
  user = get_object_or_404(User, id=id)
  email = user.email
  send_otp_via_mail.delay(email)
  otp_timer.apply_async((email, ), countdown = 600)
  return Response({
    'status':200,
    'message':'OTP sent sucessfully, Expires in 5min.'
  }, status.HTTP_200_OK)


@api_view(['GET'])
def all_users(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response({
    'status':200,
    'Message':"List of all users",
    'data':serializer.data
  }, status.HTTP_200_OK)

