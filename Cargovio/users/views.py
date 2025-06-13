from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserTypeForm, CompanyRegistrationForm, CarrierRegistrationForm
from .models import Company, Carrier

def register(request):
    if request.method == 'POST':
        if 'user_type' in request.POST:
            # First step: user type selection
            form = UserTypeForm(request.POST)
            if form.is_valid():
                user_type = form.cleaned_data['user_type']
                request.session['user_type'] = user_type
                return redirect('users:register_details')
        else:
            # Second step: registration details
            user_type = request.session.get('user_type')
            if user_type == 'company':
                form = CompanyRegistrationForm(request.POST)
            else:
                form = CarrierRegistrationForm(request.POST)

            if form.is_valid():
                user = form.save()
                if user_type == 'company':
                    company = Company.objects.create(
                        user=user,
                        company_name=form.cleaned_data['company_name'],
                        description=form.cleaned_data['description'],
                        address=form.cleaned_data['address'],
                        phone_number=form.cleaned_data['phone_number']
                    )
                else:
                    carrier = Carrier.objects.create(
                        user=user,
                        company_name=form.cleaned_data['company_name'],
                        vehicle_type=form.cleaned_data['vehicle_type'],
                        vehicle_capacity=form.cleaned_data['vehicle_capacity'],
                        address=form.cleaned_data['address'],
                        phone_number=form.cleaned_data['phone_number']
                    )
                
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('core:home')
    else:
        # First step: show user type selection
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
