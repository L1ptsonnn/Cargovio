from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

class Company(AbstractBaseUser):
    company_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(region='UA')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'phone_number']

    def get_username(self):
        return self.email

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
    # Особиста інформація
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region='UA')
    password = models.CharField(max_length=128)
    
    # Інформація про транспорт
    vehicle_model = models.CharField(max_length=100)
    
    # Додаткова інформація
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'vehicle_model']

    def get_username(self):
        return self.email

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.get_full_name()} - {self.vehicle_model}"
