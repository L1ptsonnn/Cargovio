from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html',
        next_page='core:home',
        http_method_names=['get', 'post']
    ), name='logout'),
    
    # Registration URLs
    path('register/', views.register, name='register'),
    path('register/details/', views.register_details, name='register_details'),
] 