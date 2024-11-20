# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from .models import User
# from .serializers import UserRegistrationSerializer, UserLoginSerializer
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# class RegisterView(APIView):

#     @swagger_auto_schema(
#         operation_description="Register a new user by providing their email, password, role, and other details.",
#         request_body=UserRegistrationSerializer,
#         responses={
#             201: openapi.Response(description="User registered successfully"),
#             400: openapi.Response(description="Invalid data or validation error")
#         }
#     )
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     @swagger_auto_schema(
#         operation_description="Login a user by providing their email and password. The role is returned upon successful login.",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email address"),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
#             },
#             required=['email', 'password']
#         ),
#         responses={
#             200: openapi.Response(description="Login successful", examples={"application/json": {"message": "Login successful", "role": "Retailer"}}),
#             401: openapi.Response(description="Invalid credentials"),
#             400: openapi.Response(description="Validation error or missing data"),
#         }
#     )
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 return Response({"message": "Login successful", "role": user.role}, status=status.HTTP_200_OK)
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
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
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful!",
                "token": token.key,
                "user": {
                    "email": user.email,
                    "role": user.role,
                    "name": user.name,
                    "contact_number": user.contact_number,
                    "address": user.address,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)