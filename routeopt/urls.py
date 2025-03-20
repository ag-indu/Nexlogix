from django.urls import path
from .views import home

app_name = 'routeopt'

urlpatterns = [
    path('', home, name='home'),  # Homepage
]
