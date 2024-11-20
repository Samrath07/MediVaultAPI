# # Create your views here.
# from rest_framework import viewsets
# # from rest_framework.permissions import IsAuthenticated
# from .models import Retailer, Wholesaler, Medicine, Inventory, Order
# from .serializers import MedicineSerializer, InventorySerializer, OrderSerializer,WholesalerProfileSerializer
# from rest_framework.response import Response
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# # from drf_spectacular.utils import extend_schema, OpenApiParameter



# # class CustomerViewSet(viewsets.ModelViewSet):
# #     queryset = Customer.objects.all()
# #     serializer_class = CustomerSerializer
# #     # permission_classes = [IsAuthenticated]  # Require authentication for this view
# # List all Wholesalers

# class CompleteWholesalerProfileView(viewsets.ViewSet):
#     @swagger_auto_schema(
#         request_body=WholesalerProfileSerializer,
#         responses={
#             200: openapi.Response(description="Profile updated successfully!"),
#             400: openapi.Response(description="Validation errors.")
#         },
#         operation_description="Allows a registered wholesaler to complete their profile by providing details such as name, email, address, city, and username.",
#         operation_summary="Complete Wholesaler Profile"
#     )
#     def post(self, request):
#         try:
#             wholesaler = Wholesaler.objects.get(user=request.user)
#         except Wholesaler.DoesNotExist:
#             return Response({"error": "Wholesaler not found"}, status=404)

#         serializer = WholesalerProfileSerializer(instance=wholesaler, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Profile updated successfully!'}, status=200)
#         return Response(serializer.errors, status=400)

# class WholesalerListView(viewsets.ModelViewSet):
#     queryset = Wholesaler.objects.filter(is_profile_complete=True)
#     serializer_class = WholesalerProfileSerializer

# # View Wholesaler's Inventory
# class WholesalerInventoryView(viewsets.ModelViewSet):
#     serializer_class = InventorySerializer

#     def get_queryset(self):
#         wholesaler_id = self.kwargs['wholesaler_id']
#         return Inventory.objects.filter(wholesaler_id=wholesaler_id)

# # Place Order
# class PlaceOrderView(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer


# # View Orders
# class OrderListView(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(wholesaler=self.request.user.wholesaler)

# # Update Order Status
# class UpdateOrderStatusView(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()

# # Manage Inventory
# class ManageInventoryView(viewsets.ModelViewSet):
#     serializer_class = InventorySerializer


# class MedicineViewSet(viewsets.ModelViewSet):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     # permission_classes = [IsAuthenticated]  # Require authentication for this view

# class InventoryViewSet(viewsets.ModelViewSet):
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer
#     # permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         wholesaler = Wholesaler.objects.get(user=self.request.user)
#         serializer.save(wholesaler=wholesaler)


# # class SupplierViewSet(viewsets.ModelViewSet):
# #     queryset = Supplier.objects.all()
# #     serializer_class = SupplierSerializer
# #     # permission_classes = [IsAuthenticated]  # Require authentication for this view

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     # permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         retailer = Retailer.objects.get(user=self.request.user)
#         serializer.save(retailer=retailer)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wholesaler, Retailer, Inventory, Medicine, Order, OrderLine,InventoryMedicine
from .serializers import InventorySerializer, OrderSerializer, WholesalerSerializer,InventoryMedicineSerializer,MedicineSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404


class InventoryView(APIView):
    def get(self, request, wholesaler_id):
        try:
            inventory = Inventory.objects.get(wholesaler__id=wholesaler_id)
            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventory.DoesNotExist:
            return Response({"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    def post(self, request):
        data = request.data
        retailer = Retailer.objects.get(user=request.user)
        wholesaler = Wholesaler.objects.get(id=data['wholesaler_id'])
        order = Order.objects.create(retailer=retailer, wholesaler=wholesaler)

        for item in data['order_lines']:
            medicine = Medicine.objects.get(id=item['medicine_id'])
            OrderLine.objects.create(order=order, medicine=medicine, quantity=item['quantity'])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class WholesalerInventoryView(APIView):
    def get(self, request):
        try:
            wholesaler = Wholesaler.objects.get(user=request.user)
            inventory = Inventory.objects.get(wholesaler=wholesaler)
            inventory_medicines = InventoryMedicine.objects.filter(inventory=inventory)
            serializer = InventoryMedicineSerializer(inventory_medicines, many=True)
            return Response({"inventory": serializer.data}, status=status.HTTP_200_OK)
        except Wholesaler.DoesNotExist:
            return Response({"error": "Wholesaler not found"}, status=status.HTTP_404_NOT_FOUND)
        except Inventory.DoesNotExist:
            return Response({"error": "No inventory found for this wholesaler"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            wholesaler = Wholesaler.objects.get(user=request.user)
            inventory, created = Inventory.objects.get_or_create(wholesaler=wholesaler)

            data = request.data
            with transaction.atomic():
                medicine, _ = Medicine.objects.get_or_create(
                    name=data['name'], brand=data['brand'], price_per_unit=data['price_per_unit']
                )
                inventory_medicine, created = InventoryMedicine.objects.get_or_create(
                    inventory=inventory, medicine=medicine
                )
                inventory_medicine.stock_level += data['stock_level']
                inventory_medicine.save()

            return Response({"message": "Medicine added to inventory successfully"}, status=status.HTTP_201_CREATED)
        except Wholesaler.DoesNotExist:
            return Response({"error": "Wholesaler not found"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, medicine_id):
        try:
            wholesaler = Wholesaler.objects.get(user=request.user)
            inventory = Inventory.objects.get(wholesaler=wholesaler)
            inventory_medicine = InventoryMedicine.objects.get(inventory=inventory, medicine__id=medicine_id)

            inventory_medicine.stock_level = request.data['stock_level']
            inventory_medicine.save()

            return Response({"message": "Stock level updated successfully"}, status=status.HTTP_200_OK)
        except Wholesaler.DoesNotExist:
            return Response({"error": "Wholesaler not found"}, status=status.HTTP_404_NOT_FOUND)
        except InventoryMedicine.DoesNotExist:
            return Response({"error": "Medicine not found in inventory"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, medicine_id):
        try:
            wholesaler = Wholesaler.objects.get(user=request.user)
            inventory = Inventory.objects.get(wholesaler=wholesaler)
            inventory_medicine = InventoryMedicine.objects.get(inventory=inventory, medicine__id=medicine_id)

            inventory_medicine.delete()
            return Response({"message": "Medicine removed from inventory successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Wholesaler.DoesNotExist:
            return Response({"error": "Wholesaler not found"}, status=status.HTTP_404_NOT_FOUND)
        except InventoryMedicine.DoesNotExist:
            return Response({"error": "Medicine not found in inventory"}, status=status.HTTP_404_NOT_FOUND)

class WholesalerListView(APIView):
    def get(self, request):
        wholesalers = Wholesaler.objects.all()
        serializer = WholesalerSerializer(wholesalers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class MedicineListView(APIView):
    def get(self, request, wholesaler_id):
        """View all medicines available with the wholesaler."""
        try:
            wholesaler = Wholesaler.objects.get(id=wholesaler_id)
            inventory = Inventory.objects.get(wholesaler=wholesaler)
            inventory_medicines = InventoryMedicine.objects.filter(inventory=inventory)
            medicine_list = [inventory_medicine.medicine for inventory_medicine in inventory_medicines]
            serializer = MedicineSerializer(medicine_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wholesaler.DoesNotExist:
            return Response({"error": "Wholesaler not found"}, status=status.HTTP_404_NOT_FOUND)
        except Inventory.DoesNotExist:
            return Response({"error": "Inventory not found for this wholesaler"}, status=status.HTTP_404_NOT_FOUND)

class OrderCreateView(APIView):
    def post(self, request):
        retailer = Retailer.objects.get(user=request.user)
        wholesaler_id = request.data.get('wholesaler')
        wholesaler = get_object_or_404(Wholesaler, id=wholesaler_id)

        # Create the order
        order_data = {
            'retailer': retailer.id,
            'wholesaler': wholesaler.id,
            'status': 'Pending', 
        }

        order_serializer = OrderSerializer(data={**order_data, **request.data})
        if order_serializer.is_valid():
            order = order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)