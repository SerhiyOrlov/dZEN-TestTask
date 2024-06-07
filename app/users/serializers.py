from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
	"""
	Serializing and deserializing Users objects
	"""
	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True
	)

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password',
			'homepage',
		)
		read_only_fields = ('access_token',)

		def update(self, instance, validated_data):
			password = validated_data.pop('password', None)
			for key, value in validated_data.items():
				setattr(instance, key, value)
			if password is not None:
				instance.set_password(password)

			instance.save()

			return instance