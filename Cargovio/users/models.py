from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Company(AbstractBaseUser):
    company_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(default='')
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'company_name'
    REQUIRED_FIELDS = ['phone_number', 'email']

    def get_username(self):
        return self.company_name

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_full_name(self):
        return self.company_name

    def get_short_name(self):
        return self.company_name

    def __str__(self):
        return self.company_name

class Carrier(AbstractBaseUser):
    company_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    vehicle_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(default='')
    address = models.TextField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'company_name'
    REQUIRED_FIELDS = ['vehicle_type', 'phone_number', 'email']

    def get_username(self):
        return self.company_name

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_full_name(self):
        return self.company_name

    def get_short_name(self):
        return self.company_name

    def __str__(self):
        return f"{self.company_name} - {self.vehicle_type}"
