from django import forms
from .models import Company, Carrier
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField

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

class CompanyRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = Company
        fields = ['company_name', 'phone_number', 'email']
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password1'])
        if commit:
            instance.save()
        return instance

class CarrierRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = Carrier
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'vehicle_model']
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password1'])
        if commit:
            instance.save()
        return instance

class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class CarrierLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 