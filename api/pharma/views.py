from .models import Customer, Medicine, Supplier, Inventory, Prescription
from .serializers import CustomerSerializer, MedicineSerializer,SupplierSerializer, InventorySerializer,PrescriptionSerializer

# Create your views here.
from rest_framework import viewsets
from .models import Customer, Medicine, Supplier, Inventory, Prescription
from .serializers import CustomerSerializer, MedicineSerializer, SupplierSerializer, InventorySerializer, PrescriptionSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer



