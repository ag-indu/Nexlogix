from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os


def demand_forecast(request):
    from .scripts.forecast import run_forecasting
    try:
        image_files = run_forecasting()  # Run the forecasting function and get image names

        # Pass images to the template
        return render(request, "demand/forecast_result.html", {"image_files": image_files, "MEDIA_URL": settings.MEDIA_URL})
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def index(request):
    return render(request, "demand/index.html")
