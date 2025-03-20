from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import BusinessRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import TruckPackingForm
from io import BytesIO
import base64
from .algorithms.space_optimization import pack_boxes_into_trucks, animate_packing, Box
from django.shortcuts import render
from django.http import JsonResponse

def register_business(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            business = form.save()
            login(request, business.owner)
            return redirect('business:dashboard')  # Redirect to dashboard after login
    else:
        form = BusinessRegistrationForm()
    return render(request, 'business/register.html', {'form': form})

def login_business(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('business:dashboard')  # Redirect to the business dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'business/login.html', {'form': form})

def logout_business(request):
    logout(request)
    return redirect('business:login')

def dashboard(request):
    return render(request, 'business/dashboard.html')

def optimize_space(request):
    if request.method == "POST":
        truck_width = int(request.POST.get("truck_width"))
        truck_height = int(request.POST.get("truck_height"))
        truck_depth = int(request.POST.get("truck_depth"))

        num_types = int(request.POST.get("num_types"))
        boxes = []

        for i in range(num_types):
            width = int(request.POST.get(f"box_width_{i}"))
            height = int(request.POST.get(f"box_height_{i}"))
            depth = int(request.POST.get(f"box_depth_{i}"))
            count = int(request.POST.get(f"box_count_{i}"))

            for _ in range(count):
                boxes.append(Box(width, height, depth, i + 1))

        # Sort boxes by volume (largest first) for better packing
        boxes.sort(key=lambda b: b.width * b.height * b.depth, reverse=True)

        # Pack boxes into trucks
        trucks = pack_boxes_into_trucks(boxes, truck_width, truck_height, truck_depth)

        # Generate animation
        animation_path = animate_packing(trucks)

        return render(request, "business/result.html", {"trucks": trucks, "animation_path": animation_path})

    return render(request, "business/packing_form.html")