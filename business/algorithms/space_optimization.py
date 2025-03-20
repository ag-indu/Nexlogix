import matplotlib.pyplot as plt
import numpy as np
import random
import time
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display, clear_output
import matplotlib.animation as animation

class Box:
    def __init__(self, width, height, depth, box_type):
        self.width = width
        self.height = height
        self.depth = depth
        self.box_type = box_type  # Identify different box types

class Truck:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.loaded_boxes = []
        self.remaining_volume = width * height * depth

    def can_fit(self, box, x, y, z):
        """Check if the box can be placed at (x, y, z) without overlapping."""
        if x + box.width > self.width or y + box.height > self.height or z + box.depth > self.depth:
            return False
       
        for loaded_box, lx, ly, lz in self.loaded_boxes:
            if not (x + box.width <= lx or lx + loaded_box.width <= x or
                    y + box.height <= ly or ly + loaded_box.height <= y or
                    z + box.depth <= lz or lz + loaded_box.depth <= z):
                return False  # Collision detected
       
        return True

    def load_box(self, box):
        """Use Bottom-Left-Back (BLB) heuristic for optimized placement."""
        positions = [(x, y, z) for x in range(self.width - box.width + 1)
                               for y in range(self.height - box.height + 1)
                               for z in range(self.depth - box.depth + 1)]
        positions.sort(key=lambda pos: (pos[1], pos[0], pos[2]))  # Sort by y, then x, then z (BLB heuristic)
       
        for x, y, z in positions:
            if self.can_fit(box, x, y, z):
                self.loaded_boxes.append((box, x, y, z))
                self.remaining_volume -= box.width * box.height * box.depth
                return True
        return False  # No space available

def pack_boxes_into_trucks(boxes, truck_width, truck_height, truck_depth):
    """Dynamically allocate trucks and load boxes using 3D bin packing."""
    trucks = [Truck(truck_width, truck_height, truck_depth)]
   
    for box in boxes:
        packed = False
        for truck in trucks:
            if truck.load_box(box):
                packed = True
                break
        if not packed:  # Need a new truck
            new_truck = Truck(truck_width, truck_height, truck_depth)
            new_truck.load_box(box)
            trucks.append(new_truck)
   
    return trucks

def animate_packing(trucks, filename="static/truck_packing.gif"):
    """Save the animation as a GIF instead of displaying it directly."""
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    color_map = {}
    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "pink", "brown"]
    
    def update(frame):
        ax.clear()
        truck_idx = frame % len(trucks)  # Loop through trucks
        truck = trucks[truck_idx]
        ax.set_title(f'Truck {truck_idx + 1}')
        
        for box, x, y, z in truck.loaded_boxes:
            if box.box_type not in color_map:
                color_map[box.box_type] = colors[len(color_map) % len(colors)]
            ax.bar3d(x, y, z, box.width, box.height, box.depth, color=color_map[box.box_type], alpha=0.7, edgecolor="black")
            ax.text(x + box.width / 2, y + box.height / 2, z + box.depth / 2, f"{box.box_type}", color="black", fontsize=8, ha="center")

        ax.set_xlabel('Width')
        ax.set_ylabel('Height')
        ax.set_zlabel('Depth')

    ani = animation.FuncAnimation(fig, update, frames=len(trucks), repeat=True)
    ani.save(filename, writer="pillow", fps=1)  # Save as GIF
    plt.close(fig)
    return filename
