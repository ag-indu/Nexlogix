from django.shortcuts import render
from .route_optimization import generate_route_map

def home(request):
    route_map = None

    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        waypoints = request.POST.get("waypoints")

        # Convert comma-separated waypoints to a list
        waypoints_list = [wp.strip() for wp in waypoints.split(",")] if waypoints else []

        # Generate optimized route map
        route_map = generate_route_map(source, destination, waypoints_list)

    return render(request, "routeopt/home.html", {"route_map": route_map})
