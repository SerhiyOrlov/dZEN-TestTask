from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
	email = serializers.CharField()
	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True
	)
	refresh_token = serializers.CharField(min_length=255, read_only=True)

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'refresh_token']

	def create(self, validated_data):
		user = User.objects.create_user(
			email=validated_data['email'],
			username=validated_data['username'],
			password=validated_data['password'],
		)
		user.refresh_token = user.refresh_token
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	username = serializers.CharField(max_length=255, read_only=True)
	password = serializers.CharField(max_length=128, write_only=True)
	access_token = serializers.SerializerMethodField()

	def get_access_token(self, obj):
		return obj.access_token

	def validate(self, data):
		email = data.get('email', None)
		password = data.get('password', None)
		print(email, password)
		if email is None:
			raise serializers.ValidationError(
				'A email address is required to log in'
			)

		if password is None:
			raise serializers.ValidationError(
				'A password is required to log in'
			)

		user = authenticate(email=email, password=password)  # Return either User model or none

		if user is None:
			raise serializers.ValidationError(
				'A user with this email and password was not found.'
			)

		if not user.is_active:
			raise serializers.ValidationError(
				'This user has benn deactivated.'
			)
		access_token = user.access_token
		return {
			'email': user.email,
			'username': user.username,
			'access_token': access_token
		}
