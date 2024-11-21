# from django.db import models
# # from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class CustomUser(models.Model):
#     ROLE_CHOICES = (
#         ('retailer', 'Retailer'),
#         ('wholesaler', 'Wholesaler'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
# class Retailer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     contact_info = models.CharField(max_length=15)
#     address = models.TextField()

# class Wholesaler(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wholesaler_profile')
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     username = models.CharField(max_length=50, unique=True)
#     is_profile_complete = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

# class Medicine(models.Model):
#     medicine_id = models.AutoField(primary_key=True)
#     medicine_name = models.CharField(max_length=100)
#     description = models.TextField()
#     brand = models.CharField(max_length=50)
#     price = models.FloatField()
#     category = models.CharField(max_length=50)
#     expiry_date = models.DateField()
#     stock_level = models.IntegerField()

#     def __str__(self):
#         return self.medicine_name
    


# class Inventory(models.Model):
#     inventory_id = models.AutoField(primary_key=True)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     stock_level = models.IntegerField()
#     reorder_level = models.IntegerField()

#     def __str__(self):
#         return f"{self.medicine.medicine_name} Inventory"

# class Order(models.Model):
#     retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
#     wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     date = models.DateTimeField(auto_now_add=True)




from django.db import models
from authentication.models import CustomUser

class Wholesaler(models.Model):
    wholesaler_name = models.TextField()
    wholesaler_contact_number = models.CharField(max_length=10)
    wholesaler_address = models.TextField(max_length=100)
    isRegistrationComplete = models.BooleanField(default=False)

    def __str__(self):
        return self.wholesaler_name


class Retailer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='retailer')
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.brand})"


class Inventory(models.Model):
    wholesaler = models.OneToOneField(Wholesaler, on_delete=models.CASCADE, related_name='inventory')
    medicines = models.ManyToManyField(Medicine, through='InventoryMedicine')

    def __str__(self):
        return f"Inventory of {self.wholesaler.name}"


class InventoryMedicine(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    stock_level = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.name} - {self.stock_level} units"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='orders')
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.retailer.name}"


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} units"

