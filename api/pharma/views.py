# Create your views here.
from rest_framework import viewsets
from .models import Customer, Medicine, Supplier, Inventory, Prescription
from .serializers import CustomerSerializer, MedicineSerializer, SupplierSerializer, InventorySerializer, PrescriptionSerializer
from rest_framework.permissions import IsAuthenticated

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for this view


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for this view


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for this view


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for this view


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for this view




