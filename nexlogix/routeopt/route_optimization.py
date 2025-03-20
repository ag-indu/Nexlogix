import googlemaps
import folium
import heapq
import math
from polyline import decode
from datetime import datetime

# Initialize Google Maps API
API_KEY = "AIzaSyBDjD9Aa7zIJ3eI4q1XVaEFKs5i-5GAbFc"  # Replace with your actual API key
gmaps = googlemaps.Client(key=API_KEY)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two latitude-longitude points."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def get_travel_times(locations):
    """Fetch travel times considering real-time traffic data."""
    travel_graph = {}
    location_coords = {}

    for loc in locations:
        geocode_result = gmaps.geocode(loc)[0]["geometry"]["location"]
        location_coords[loc] = (geocode_result["lat"], geocode_result["lng"])
        travel_graph[loc] = {}

        distances = gmaps.distance_matrix(
            origins=[loc], destinations=locations, mode="driving", departure_time="now"
        )["rows"][0]["elements"]

        for i, dest in enumerate(locations):
            if loc != dest and distances[i]["status"] == "OK":
                travel_graph[loc][dest] = distances[i]["duration"]["value"] // 60  # Convert to minutes

    return travel_graph, location_coords


def a_star(source, destination, locations, travel_graph, location_coords):
    """Find the shortest route using the A* algorithm."""
    priority_queue = []
    heapq.heappush(priority_queue, (0, [source]))  # (cost, path)
    visited = set()
    
    while priority_queue:
        current_cost, current_path = heapq.heappop(priority_queue)
        current_location = current_path[-1]
        
        if current_location in visited:
            continue
        visited.add(current_location)
        
        if current_location == destination:
            return current_path, current_cost
        
        for neighbor, travel_time in travel_graph[current_location].items():
            if neighbor not in visited:
                heuristic = haversine(*location_coords[neighbor], *location_coords[destination])
                total_cost = current_cost + travel_time + heuristic
                heapq.heappush(priority_queue, (total_cost, current_path + [neighbor]))
    
    return None, float('inf')

def generate_route_map(source, destination, waypoints=[]):
    """Generate an optimized route map using A* algorithm."""
    locations = [source] + waypoints + [destination]
    travel_graph, location_coords = get_travel_times(locations)
    
    # Ensure waypoints are included in order
    current_source = source
    full_path = []
    total_time = 0

    for waypoint in waypoints + [destination]:
        path_segment, time_segment = a_star(current_source, waypoint, locations, travel_graph, location_coords)
        if path_segment:
            full_path.extend(path_segment[:-1])  # Exclude duplicate points
            total_time += time_segment
            current_source = waypoint  # Move source to next waypoint

    full_path.append(destination)  # Add final destination
    optimal_path, optimal_time = full_path, total_time

    
    first_location = location_coords[source]
    route_map = folium.Map(location=[first_location[0], first_location[1]], zoom_start=12)
    
    for i in range(len(optimal_path) - 1):
        origin, destination = optimal_path[i], optimal_path[i + 1]
        route = gmaps.directions(origin, destination, mode="driving", departure_time="now")

        if route:
            polyline_points = route[0]["overview_polyline"]["points"]
            decoded_points = decode(polyline_points)
            folium.PolyLine(decoded_points, color="blue", weight=5, opacity=0.7).add_to(route_map)
    
    for i, loc in enumerate(optimal_path):
        lat, lng = location_coords[loc]
        marker_color = "green" if i == 0 else "red" if i == len(optimal_path) - 1 else "blue"
        popup_text = f"{loc} (Start)" if i == 0 else f"{loc} (End) - Reached in {optimal_time} mins" if i == len(optimal_path) - 1 else loc
        
        folium.Marker([lat, lng], popup=popup_text, icon=folium.Icon(color=marker_color)).add_to(route_map)
    
    return route_map._repr_html_()
