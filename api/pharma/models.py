from django.db import models

# Create your models here.

class Customer(models.Model):
    GENDER_CHOICE = [
        (True, 'MALE'),
        (False, 'FEMALE')
    ]
    customer_id = models.AutoField(primary_key= True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.BooleanField(choices=GENDER_CHOICE)
    age = models.IntegerField()
    prescription_detail = models.TextField()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.CharField(max_length=50)
    expiry_date = models.DateField()
    stock_level = models.IntegerField()

    def __str__(self):
        return self.medicine_name
    

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.supplier_name

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    stock_level = models.IntegerField()
    reorder_level = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.medicine_name} Inventory"

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    date = models.DateField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.IntegerField()

    def __str__(self):
        return f"Prescription {self.prescription_id} for {self.customer}"





