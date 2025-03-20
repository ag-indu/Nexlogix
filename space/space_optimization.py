import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display, clear_output

class Box:
    def __init__(self, width, height, depth, box_type):
        self.width = width
        self.height = height
        self.depth = depth
        self.box_type = box_type

class Truck:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.loaded_boxes = []
        self.remaining_volume = width * height * depth

    def can_fit(self, box, x, y, z):
        if x + box.width > self.width or y + box.height > self.height or z + box.depth > self.depth:
            return False

        for loaded_box, lx, ly, lz in self.loaded_boxes:
            if not (x + box.width <= lx or lx + loaded_box.width <= x or
                    y + box.height <= ly or ly + loaded_box.height <= y or
                    z + box.depth <= lz or lz + loaded_box.depth <= z):
                return False

        return True

    def load_box(self, box):
        positions = [(x, y, z) for x in range(self.width - box.width + 1)
                               for y in range(self.height - box.height + 1)
                               for z in range(self.depth - box.depth + 1)]
        positions.sort(key=lambda pos: (pos[1], pos[0], pos[2]))

        for x, y, z in positions:
            if self.can_fit(box, x, y, z):
                self.loaded_boxes.append((box, x, y, z))
                self.remaining_volume -= box.width * box.height * box.depth
                return True
        return False

def pack_boxes_into_trucks(boxes, truck_width, truck_height, truck_depth):
    trucks = [Truck(truck_width, truck_height, truck_depth)]

    for box in boxes:
        packed = False
        for truck in trucks:
            if truck.load_box(box):
                packed = True
                break
        if not packed:
            new_truck = Truck(truck_width, truck_height, truck_depth)
            new_truck.load_box(box)
            trucks.append(new_truck)

    return trucks

def animate_packing(trucks):
    color_map = {}
    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "pink", "brown"]

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Width')
    ax.set_ylabel('Height')
    ax.set_zlabel('Depth')

    for truck_idx, truck in enumerate(trucks):
        ax.clear()
        ax.set_title(f'Truck {truck_idx + 1}')

        for j, (box, x, y, z) in enumerate(truck.loaded_boxes):
            if box.box_type not in color_map:
                color_map[box.box_type] = colors[len(color_map) % len(colors)]
            ax.bar3d(x, y, z, box.width, box.height, box.depth, color=color_map[box.box_type], alpha=0.7, edgecolor="black")
            ax.text(x + box.width / 2, y + box.height / 2, z + box.depth / 2, f"{box.box_type}", color="black", fontsize=8, ha="center")

            plt.pause(0.3)
            display(fig)
            clear_output(wait=True)

    plt.show()
def visualize_all_trucks(trucks):
    """Visualize all trucks in a single figure with subplots and a legend."""
    num_trucks = len(trucks)
    cols = min(3, num_trucks)  # Limit to 3 columns per row
    rows = (num_trucks + cols - 1) // cols  # Compute required rows
    
    fig = plt.figure(figsize=(5 * cols, 5 * rows))  # Adjust figure size dynamically
    
    color_map = {}  # Store box type colors
    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "pink", "brown"]

    # Assign colors to box types
    for truck in trucks:
        for box, _, _, _ in truck.loaded_boxes:
            if box.box_type not in color_map:
                color_map[box.box_type] = colors[len(color_map) % len(colors)]  # Assign unique colors

    for i, truck in enumerate(trucks):
        ax = fig.add_subplot(rows, cols, i + 1, projection='3d')
        
        for box, x, y, z in truck.loaded_boxes:
            ax.bar3d(x, y, z, box.width, box.height, box.depth, 
                     color=color_map[box.box_type], alpha=0.6, edgecolor="black")
            ax.text(x + box.width / 2, y + box.height / 2, z + box.depth / 2, 
                    f"{box.box_type}", color="black", fontsize=8, ha="center")

        ax.set_xlabel('Width')
        ax.set_ylabel('Height')
        ax.set_zlabel('Depth')
        ax.set_title(f'Truck {i+1}')

    # Create Legend
    legend_fig, legend_ax = plt.subplots(figsize=(4, len(color_map) * 0.5))
    legend_ax.axis("off")

    for i, (box_type, color) in enumerate(color_map.items()):
        legend_ax.add_patch(plt.Rectangle((0, i), 1, 1, color=color, alpha=0.6))
        legend_ax.text(1.2, i + 0.5, f"Box Type {box_type}", va='center', fontsize=10)

    legend_ax.set_xlim(0, 3)
    legend_ax.set_ylim(0, len(color_map))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Read command-line arguments passed from Django
    truck_width = int(sys.argv[1])
    truck_height = int(sys.argv[2])
    truck_depth = int(sys.argv[3])
    num_types = int(sys.argv[4])

    boxes = []
    index = 5  # Start reading box data after the first 4 arguments
    for i in range(num_types):
        width = int(sys.argv[index])
        height = int(sys.argv[index+1])
        depth = int(sys.argv[index+2])
        count = int(sys.argv[index+3])
        index += 4

        for _ in range(count):
            boxes.append(Box(width, height, depth, i+1))

    # Sort boxes by volume (largest first) for better packing
    boxes.sort(key=lambda b: b.width * b.height * b.depth, reverse=True)

    # Pack boxes into trucks
    trucks = pack_boxes_into_trucks(boxes, truck_width, truck_height, truck_depth)

    # Print output to console (Django will not display this)
    print(f"\nTotal Trucks Needed: {len(trucks)}")

    # Run animation (opens in a new window)
    animate_packing(trucks)
    visualize_all_trucks(trucks)