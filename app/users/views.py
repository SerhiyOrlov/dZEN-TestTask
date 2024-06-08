from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action

from .models import User

from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

from core.permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ViewSet):
	permission_classes = ()

	def get_permissions(self):
		# Set permissions depending on the request
		match self.action:
			case "retrieve":
				permission_classes = [AllowAny]
			case "update":
				permission_classes = [IsOwnerOrAdmin]
			case _:
				permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]

	def retrieve(self, request, username=None):
		user = get_object_or_404(User, username=username)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def update(self, request, pk=None):

		user = get_object_or_404(User, pk=pk)
		serializer = UserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


