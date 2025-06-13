from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Carrier

class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('company', 'Company'),
        ('carrier', 'Carrier'),
    ]
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label='Register as'
    )

class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CarrierRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    vehicle_type = forms.CharField(max_length=50)
    vehicle_capacity = forms.DecimalField(max_digits=10, decimal_places=2)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') 