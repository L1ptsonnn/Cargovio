from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserTypeForm, CompanyRegistrationForm, CarrierRegistrationForm, CompanyLoginForm, CarrierLoginForm
from .models import Company, Carrier
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'company':
            form = CompanyRegistrationForm(request.POST)
            if form.is_valid():
                company = form.save()
                request.session['company_id'] = company.id
                request.session['company_name'] = company.company_name
                return JsonResponse({'success': True, 'redirect': '/'})
            else:
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        elif user_type == 'carrier':
            form = CarrierRegistrationForm(request.POST)
            if form.is_valid():
                carrier = form.save()
                request.session['carrier_id'] = carrier.id
                request.session['carrier_name'] = carrier.company_name
                return JsonResponse({'success': True, 'redirect': '/'})
            else:
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        else:
            return JsonResponse({'success': False, 'error': 'User type required'})
    else:
        form = UserTypeForm()
        return render(request, 'users/register.html', {'form': form})

def register_details(request):
    user_type = request.session.get('user_type')
    if not user_type:
        return redirect('users:register')
    
    if request.method == 'POST':
        if user_type == 'company':
            form = CompanyRegistrationForm(request.POST)
        else:
            form = CarrierRegistrationForm(request.POST)
    else:
        if user_type == 'company':
            form = CompanyRegistrationForm()
        else:
            form = CarrierRegistrationForm()
    
    return render(request, 'users/register_details.html', {
        'form': form,
        'user_type': user_type
    })

def is_authenticated(request):
    return bool(request.session.get('company_id') or request.session.get('carrier_id'))

@login_required(login_url='/users/login/')
def profile(request):
    company_id = request.session.get('company_id')
    carrier_id = request.session.get('carrier_id')
    company = carrier = None
    if company_id:
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            pass
    if carrier_id:
        try:
            carrier = Carrier.objects.get(id=carrier_id)
        except Carrier.DoesNotExist:
            pass
    return render(request, 'users/profile.html', {'company': company, 'carrier': carrier})

def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'company':
            form = CompanyLoginForm(request.POST)
            if form.is_valid():
                try:
                    company = Company.objects.get(company_name=form.cleaned_data['company_name'], phone_number=form.cleaned_data['phone_number'])
                    if check_password(form.cleaned_data['password'], company.password):
                        request.session['company_id'] = company.id
                        request.session['company_name'] = company.company_name
                        return JsonResponse({'success': True, 'redirect': '/'})
                    else:
                        return JsonResponse({'success': False, 'error': 'Invalid credentials'})
                except Company.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'})
            else:
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        elif user_type == 'carrier':
            form = CarrierLoginForm(request.POST)
            if form.is_valid():
                try:
                    carrier = Carrier.objects.get(company_name=form.cleaned_data['company_name'], vehicle_type=form.cleaned_data['vehicle_type'], phone_number=form.cleaned_data['phone_number'])
                    if check_password(form.cleaned_data['password'], carrier.password):
                        request.session['carrier_id'] = carrier.id
                        request.session['carrier_name'] = carrier.company_name
                        return JsonResponse({'success': True, 'redirect': '/'})
                    else:
                        return JsonResponse({'success': False, 'error': 'Invalid credentials'})
                except Carrier.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'})
            else:
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        else:
            return JsonResponse({'success': False, 'error': 'User type required'})
    else:
        form = UserTypeForm()
        return render(request, 'users/login.html', {'form': form})
