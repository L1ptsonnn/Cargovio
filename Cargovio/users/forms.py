from django import forms
from .models import Company, Carrier
from django.contrib.auth.hashers import make_password
from phonenumber_field.formfields import PhoneNumberField

class CompanyRegistrationForm(forms.ModelForm):
    company_name = forms.CharField(
        label="Назва компанії",
        widget=forms.TextInput(attrs={'placeholder': 'ТОВ "Роги та копита"'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'contact@company.com'})
    )
    phone_number = forms.CharField(
        label="Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380...'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введіть надійний пароль'})
    )
    password_confirm = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'})
    )

    class Meta:
        model = Company
        fields = ['company_name', 'email', 'phone_number', 'password', 'password_confirm']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Паролі не співпадають.")
        return password_confirm

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance

class CarrierRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Повне ім'я",
        widget=forms.TextInput(attrs={'placeholder': 'Іван Петренко'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'ivan.petrenko@email.com'})
    )
    phone_number = forms.CharField(
        label="Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380...'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введіть надійний пароль'})
    )
    password_confirm = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторіть пароль'})
    )

    class Meta:
        model = Carrier
        fields = ['full_name', 'email', 'phone_number', 'password', 'password_confirm']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Паролі не співпадають.")
        return password_confirm

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance

class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class CarrierLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 