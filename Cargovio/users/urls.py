from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html',
        next_page='core:home',
        http_method_names=['get', 'post']
    ), name='logout'),

    path('register/', views.register, name='register'),
    path('register/details/', views.register_details, name='register_details'),
    path('profile/', views.profile, name='profile'),
] 