from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import CustomerViewSet, MedicineViewSet, SupplierViewSet, InventoryViewSet, PrescriptionViewSet


router = DefaultRouter()

router.register(r'customers', CustomerViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'prescriptions', PrescriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]