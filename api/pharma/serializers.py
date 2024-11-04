from rest_framework import serializers
from .models import Customer, Medicine, Supplier, Inventory, Prescription
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes



@permission_classes([IsAuthenticated])
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
