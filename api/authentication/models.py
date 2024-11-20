# from django.contrib.auth.models import User
# from django.db import models

# class User(User):
#     ROLE_CHOICES = (
#         ('Retailer', 'Retailer'),
#         ('Wholesaler', 'Wholesaler'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     # email = models.EmailField(unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return f"{self.email} ({self.role})"
# from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[('Retailer', 'Retailer'), ('Wholesaler', 'Wholesaler')])
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    username = models.CharField(max_length=20)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'name', 'contact_number', 'address']

    def __str__(self):
        return f"{self.email} ({self.role})"
