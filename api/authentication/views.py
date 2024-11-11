# auth/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "User registered successfully", 400: "Bad Request"},
        operation_description="Register a new user with username, email, password, first name, and last name.",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "refresh": "<refresh_token>",
                        "access": "<access_token>"
                    }
                }
            ),
            401: "Unauthorized - Invalid credentials",
            400: "Bad Request - Missing parameters"
        },
        operation_description="Authenticate a user and return access and refresh tokens."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
