from django.urls import path
from . import views
from .views import space_optimization_view


urlpatterns = [
     path('', space_optimization_view, name='space_optimization_view'),  # Default route for space optimization
]