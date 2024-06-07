# views.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegistrationSerializer, LoginSerializer
from .utils import JWTManager

from users.models import User


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    jwt_manager = JWTManager()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'access_token': user.access_token}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({f'access_token': user.get('access_token')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        access_token = request.data.get('access_token')
        access_token = self.jwt_manager.refresh_token(old_token=access_token)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)



