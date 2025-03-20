from django.urls import path
from .views import register_business,login_business, logout_business,dashboard,optimize_space

app_name = 'business'

urlpatterns = [
    path('register/', register_business, name='register_business'),
    path('login/', login_business, name='login'),
    path('logout/', logout_business, name='logout'),
    path('dashboard/',dashboard, name='dashboard'),
    path('space-optimization/', optimize_space, name='space_optimization'),
 
]


