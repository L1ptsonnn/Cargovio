from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegistrationForm, CarrierRegistrationForm, CompanyLoginForm, CarrierLoginForm
from .models import Company, Carrier

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'company':
            form = CompanyRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user, backend='users.auth_backend.CompanyAuthBackend')
                messages.success(request, f'Вітаємо, компанія "{user.company_name}" успішно зареєстрована!')
                return redirect('core:home')
            else:
                # Передаємо обидві форми назад, але тільки одна буде з помилками
                carrier_form = CarrierRegistrationForm()
        elif user_type == 'carrier':
            form = CarrierRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user, backend='users.auth_backend.CarrierAuthBackend')
                messages.success(request, f'Вітаємо, {user.full_name}, ви успішно зареєстровані як перевізник!')
                return redirect('core:home')
            else:
                # Передаємо обидві форми назад
                company_form = CompanyRegistrationForm()
        
        # Якщо валідація не пройдена, рендеримо сторінку знову з помилками
        context = {
            'company_form': form if user_type == 'company' else company_form,
            'carrier_form': form if user_type == 'carrier' else carrier_form
        }
        return render(request, 'users/register.html', context)

    # Для GET запиту
    company_form = CompanyRegistrationForm()
    carrier_form = CarrierRegistrationForm()
    context = {
        'company_form': company_form,
        'carrier_form': carrier_form
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'company':
            form = CompanyLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('company_name')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password, user_type='company')
                if user is not None:
                    auth_login(request, user, backend='users.auth_backend.CompanyAuthBackend')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Неправильна назва компанії або пароль.')
            
        elif user_type == 'carrier':
            form = CarrierLoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=email, password=password, user_type='carrier')
                if user is not None:
                    auth_login(request, user, backend='users.auth_backend.CarrierAuthBackend')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Неправильний email або пароль.')
        else:
            messages.error(request, 'Будь ласка, виберіть тип користувача.')
        
        # Якщо щось пішло не так, повертаємо на сторінку логіну
        # Модальне вікно має самостійно обробляти показ помилок
        return redirect('core:home')

    # GET-запит не має сенсу для логіну, оскільки він у модальному вікні,
    # але ми залишимо редирект на головну сторінку.
    return redirect('core:home')


@login_required
def profile(request):
    # The user object on the request is now the custom user (Company or Carrier)
    # due to our custom authentication backend.
    user = request.user
    user_type = 'company' if isinstance(user, Company) else 'carrier'
    
    return render(request, 'users/profile.html', {
        'user': user,
        'user_type': user_type
    })


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Ви успішно вийшли з системи.")
    return redirect('core:home')
