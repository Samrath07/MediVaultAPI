# from rest_framework.routers import DefaultRouter
# from django.urls import path, include
# from .views import (
#     MedicineViewSet, InventoryViewSet, OrderViewSet,
#     WholesalerListView, WholesalerInventoryView,
#     PlaceOrderView, ManageInventoryView, UpdateOrderStatusView,
#     CompleteWholesalerProfileView
# )

# # Create a router and register the ViewSets
# router = DefaultRouter()
# router.register(r'medicines', MedicineViewSet, basename='medicines')
# router.register(r'inventories', InventoryViewSet, basename='inventories')
# router.register(r'orders', OrderViewSet, basename='orders')

# # Define additional endpoints for custom views
# urlpatterns = [
#     path('wholesalers/', WholesalerListView.as_view({'get': 'list'}), name='wholesalers'),
#     path('wholesalers/<int:wholesaler_id>/inventory/', WholesalerInventoryView.as_view({'get': 'list'}), name='wholesaler_inventory'),
#     path('place-order/', PlaceOrderView.as_view({'post': 'create'}), name='place_order'),
#     path('manage-inventory/', ManageInventoryView.as_view({'post': 'create'}), name='manage_inventory'),
#     path('orders/<int:order_id>/', UpdateOrderStatusView.as_view({'put': 'update'}), name='update_order_status'),
#     path('wholesaler/profile/', CompleteWholesalerProfileView.as_view({'post' : 'create'}), name='complete_wholesaler_profile'),
#     path('', include(router.urls)), 
# ]
from django.urls import path
from .views import InventoryView, OrderCreateView, WholesalerInventoryView,WholesalerListView,MedicineListView

urlpatterns = [
    # path('inventory/', WholesalerInventoryView.as_view(), name='view_inventory'),
    path('wholesalers/', WholesalerListView.as_view(), name='wholesaler_list'),
    path('wholesalers/<int:wholesaler_id>/medicines/', MedicineListView.as_view(), name='wholesaler_medicines'),
    path('inventory/add/', WholesalerInventoryView.as_view(), name='add_inventory'),
    path('inventory/update/<int:medicine_id>/', WholesalerInventoryView.as_view(), name='update_inventory'),
    path('inventory/delete/<int:medicine_id>/', WholesalerInventoryView.as_view(), name='delete_inventory'),
    path('inventory/<int:wholesaler_id>/', InventoryView.as_view(), name='inventory'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
]
