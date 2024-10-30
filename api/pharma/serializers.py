from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Customer, Medicine, Supplier, Inventory, Prescription



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        email = serializers.EmailField(
            required=True,
            validators = [UniqueValidator(queryset=User.objects.all())]
        )
        password = serializers.CharField(
            write_only=True, required=True, validators=[validate_password]
        )
        password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__' 

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'
