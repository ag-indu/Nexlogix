from django.shortcuts import render
import subprocess
from .forms import SpaceOptimizationForm

def space_optimization_view(request):
    if request.method == 'POST':
        form = SpaceOptimizationForm(request.POST, num_types=int(request.POST.get('num_types', 1)))
        if form.is_valid():
            truck_width = form.cleaned_data['truck_width']
            truck_height = form.cleaned_data['truck_height']
            truck_depth = form.cleaned_data['truck_depth']
            num_types = form.cleaned_data['num_types']

            box_data = []
            for i in range(1, num_types + 1):
                width = form.cleaned_data[f'width_{i}']
                height = form.cleaned_data[f'height_{i}']
                depth = form.cleaned_data[f'depth_{i}']
                count = form.cleaned_data[f'count_{i}']
                box_data.append((width, height, depth, count))

            # Construct the command with all arguments
            command = ["python", "space/space_optimization.py", 
                       str(truck_width), str(truck_height), str(truck_depth), str(num_types)] + \
                      [str(item) for sublist in box_data for item in sublist]

            # Run the script and capture output
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Extract the number of trucks from the script output
            output_lines = result.stdout.split("\n")
            num_trucks = "Unknown"
            for line in output_lines:
                if "Total Trucks Needed:" in line:
                    num_trucks = line.split(":")[-1].strip()

            return render(request, 'space/result.html', {'num_trucks': num_trucks, 'message': "Animation running in a new window!"})

    else:
        form = SpaceOptimizationForm()

    return render(request, 'space/form.html', {'form': form})
