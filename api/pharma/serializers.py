# from rest_framework import serializers
# from .models import User, Retailer, Wholesaler, Medicine, Inventory, Order

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'role', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

# class RetailerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Retailer
#         fields = '__all__'

# class WholesalerProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wholesaler
#         fields = '__all__'

#     def update(self, instance, validated_data):
#         validated_data['is_profile_complete'] = True  # Mark profile as complete
#         return super().update(instance, validated_data)
# class MedicineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Medicine
#         fields = '__all__'

# class InventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Inventory
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
from rest_framework import serializers
from .models import Wholesaler, Retailer, Medicine, Inventory, InventoryMedicine, Order, OrderLine

from rest_framework import serializers
from .models import CustomUser, Wholesaler


class WholesalerRegistrationSerializer(serializers.Serializer):

    wholesaler_name = serializers.CharField(max_length=100)
    wholesaler_contact_number = serializers.CharField(max_length=15)
    wholesaler_address = serializers.CharField()
    isRegistrationComplete = serializers.BooleanField(default = False)
    
    def create(self, validated_data):
        # user_data = {
        #     # "email": validated_data.get("email"),
        #     # "username": validated_data.get("username"),
        #     # "password": validated_data.get("password"),
        #     # "role": validated_data.get("role"),
        #     "name": validated_data.get("wholesaler_name"),
        #     "contact_number": validated_data.get("wholesaler_contact_number"),
        #     "address": validated_data.get("wholesaler_address"),
        #     "isRegistrationComplete" : validated_data.get('isRegistrationComplete')
        # }

        # Create a new CustomUser
        # user = CustomUser.objects.create_user(
        #     email=user_data["email"],
        #     username=user_data["username"],
        #     password=user_data["password"],
        #     role=user_data["role"],
        #     # name=user_data["name"],
        #     # contact_number=user_data["contact_number"],
        #     # address=user_data["address"],
            
        # )

        # Extract and create Wholesaler data
        wholesaler_data = {
            # "user": user,
            "wholesaler_name": validated_data.get("wholesaler_name"),
            "wholesaler_contact_number": validated_data.get("wholesaler_contact_number"),
            "wholesaler_address": validated_data.get("wholesaler_address"),
            "isRegistrationComplete" : validated_data.get('isRegistrationComplete')
        }
        wholesaler = Wholesaler.objects.create(**wholesaler_data)

        return wholesaler

class RetailerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Retailer
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'brand', 'price_per_unit']


class InventoryMedicineSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer()

    class Meta:
        model = InventoryMedicine
        fields = ['medicine', 'stock_level']


class InventorySerializer(serializers.ModelSerializer):
    medicines = InventoryMedicineSerializer(source='inventorymedicine_set', many=True)

    class Meta:
        model = Inventory
        fields = ['id', 'wholesaler', 'medicines']


class OrderLineSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer()

    class Meta:
        model = OrderLine
        fields = ['medicine', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'retailer', 'wholesaler', 'order_date', 'status', 'order_lines']

    def create(self, validated_data):
        order_lines_data = validated_data.pop('order_lines')
        order = Order.objects.create(**validated_data)
        for order_line_data in order_lines_data:
            medicine = Medicine.objects.get(id=order_line_data['medicine_id'])
            OrderLine.objects.create(order=order, medicine=medicine, **order_line_data)
        return order

class WholesalerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wholesaler
        fields = '__all__'