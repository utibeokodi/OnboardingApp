from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from accounts.serializers import LoginSerializer
from accounts.serializers import ResetSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
import string
import secrets
from django.core.mail import EmailMessage
from datetime import datetime
from datetime import timedelta

#view for registration of users
class UserCreate(generics.CreateAPIView):
	queryset = CustomUser.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = UserSerializer
	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			user.is_active = True
			user.save()
			if user:
				return Response({'data':'Your Account has been created Succesfully'}, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#view for authentication of users			
class LoginView(generics.CreateAPIView):
	queryset = CustomUser.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = LoginSerializer
	def post(self, request, format='json'):
		email = request.data.get("email")
		password = request.data.get("password")
		remember_me = request.data.get("remember_me")
		if email is None or password is None:
			return Response({'error':'Please provide a valid credential'}, status=status.HTTP_400_BAD_REQUEST)
		user = authenticate(email=email, password=password)
		if not user:
			return Response({'error':'Invalid Credentials'}, status = status.HTTP_404_NOT_FOUND)
		token, _ = Token.objects.get_or_create(user=user)
		create_date = str(user.date_joined)
		data = {'token':token.key, 'user_id':user.id, 'email':user.email, 'create_date':create_date}
		return Response(data, status = status.HTTP_200_OK)
	

def create_password():
	alphabet = string.ascii_letters + string.digits
	password = ''.join(secrets.choice(alphabet) for i in range(12))
	return password
	
#view for Reset of user password	
class ResetPassword(generics.CreateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = ResetSerializer
	authentication_classes = (TokenAuthentication,) 
	permission_classes = (AllowAny,)
	def post(self, request, format='json'):
		email = request.data.get('email')
		if email and CustomUser.objects.filter(email=email).exists():
			password = create_password()
			user = CustomUser.objects.get(email=email)
			user.set_password(password)
			user.save()
			body = """
			 Hello %s,\n
			 Your Email is %s\n
			 Your new password is %s\n
			 Regards,\n
			""" % (email, email, password)
			mail = EmailMessage('Password Reset', body, 'Utibe Okodi <noreply@utibeokodi.com>', [email])
			mail.content_subtype = "html"
			mail.send()
			return Response({'data':'Your Password has been changed succesfully'}, status = status.HTTP_200_OK)
		if email is None or CustomUser.objects.filter(email=email).exists() == False:
			return Response({},status = status.HTTP_400_BAD_REQUEST)
		
		