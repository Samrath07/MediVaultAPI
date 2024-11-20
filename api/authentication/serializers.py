# from rest_framework import serializers
# from .models import User
# from django.contrib.auth.hashers import make_password

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'role']

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
# auth/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    email = serializers.CharField(min_length = 10)
    password = serializers.CharField(write_only = True, min_length = 5)
    role = serializers.CharField()
    name = serializers.CharField(min_length = 8)
    contact_number = serializers.IntegerField()
    address = serializers.CharField(min_length = 10)


    class Meta:
        model = CustomUser
        fields = ['username','email', 'password', 'role', 'name', 'contact_number', 'address']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            name=validated_data['name'],
            contact_number=validated_data['contact_number'],
            address=validated_data['address']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if user.role != role:
            raise serializers.ValidationError("Role mismatch.")
        
        data['user'] = user
        return data