from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Carrier(models.Model):
    company_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    vehicle_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.vehicle_type}"
