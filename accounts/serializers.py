from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from rest_framework import generics

class UserSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, validators = [UniqueValidator(queryset=CustomUser.objects.all())])
	password = serializers.CharField(min_length=8)
	class Meta:
		model = CustomUser
		fields = ['email', 'password']
		extra_kwargs = {'password':{'write_only':True}}
		
	def create(self, validated_data):
		user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'])
		return user
		
class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, validators = [UniqueValidator(queryset=CustomUser.objects.all())])
	password = serializers.CharField(min_length=8)
	remember_me = serializers.BooleanField()
	class Meta:
		model = CustomUser
		fields = ['email', 'password', 'remember_me']
		extra_kwargs = {'password':{'write_only':True}}
		
class ResetSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, validators = [UniqueValidator(queryset=CustomUser.objects.all())])
	class Meta:
		model = CustomUser
		fields = ['email']
		

	