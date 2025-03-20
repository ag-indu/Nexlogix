from django.urls import path
from .views import index,demand_forecast

urlpatterns = [
    path("", index, name="index"),
    path("forecast/", demand_forecast, name="demand_forecast"),
]
