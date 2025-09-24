import tkinter as tk
import math
import random
import colorsys

class FlowingSpheres:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flowing Connected Spheres")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Sphere parameters
        self.num_spheres = 8
        self.spheres = []
        self.t = 0
        
        # Initialize spheres
        for i in range(self.num_spheres):
            sphere = {
                'base_x': 400 + i * 60 - (self.num_spheres * 30),
                'base_y': 300,
                'offset_x': random.uniform(-50, 50),
                'offset_y': random.uniform(-50, 50),
                'phase_x': random.uniform(0, math.pi * 2),
                'phase_y': random.uniform(0, math.pi * 2),
                'freq_x': random.uniform(0.5, 2.0),
                'freq_y': random.uniform(0.5, 2.0),
                'radius': random.uniform(30, 50),
                'hue_offset': i / self.num_spheres
            }
            self.spheres.append(sphere)
        
        self.animate()
    
    def create_gradient_circle(self, x, y, radius, hue):
        """Create a circle with radial gradient effect"""
        # Create multiple concentric circles for gradient effect
        layers = 8
        for layer in range(layers, 0, -1):
            r = radius * (layer / layers)
            # Calculate color with varying saturation and brightness
            sat = 0.8 + 0.2 * (layer / layers)
            val = 0.4 + 0.6 * (layer / layers)
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline=color
            )
    
    def draw_connection(self, sphere1, sphere2, alpha=0.3):
        """Draw flowing connection between two spheres"""
        x1, y1 = sphere1['current_x'], sphere1['current_y']
        x2, y2 = sphere2['current_x'], sphere2['current_y']
        
        # Calculate connection color (blend of both sphere colors)
        hue1 = (sphere1['hue_offset'] + self.t * 0.01) % 1.0
        hue2 = (sphere2['hue_offset'] + self.t * 0.01) % 1.0
        avg_hue = (hue1 + hue2) / 2
        
        rgb = colorsys.hsv_to_rgb(avg_hue, 0.6, 0.5)
        color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        
        # Draw flowing connection with varying width
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance < 150:  # Only connect nearby spheres
            # Create flowing connection with sine wave
            segments = 20
            points = []
            
            for i in range(segments + 1):
                t_seg = i / segments
                x = x1 + (x2 - x1) * t_seg
                y = y1 + (y2 - y1) * t_seg
                
                # Add flowing wave effect
                perpendicular_x = -(y2 - y1) / distance if distance > 0 else 0
                perpendicular_y = (x2 - x1) / distance if distance > 0 else 0
                
                wave_amplitude = 10 * math.sin(self.t * 0.1 + t_seg * math.pi * 2)
                x += perpendicular_x * wave_amplitude
                y += perpendicular_y * wave_amplitude
                
                points.extend([x, y])
            
            if len(points) > 4:
                self.canvas.create_line(points, fill=color, width=3, smooth=True)
    
    def update_positions(self):
        """Update sphere positions with organic movement"""
        for i, sphere in enumerate(self.spheres):
            # Organic movement using multiple sine waves
            x_movement = (
                sphere['offset_x'] * math.sin(self.t * 0.02 * sphere['freq_x'] + sphere['phase_x']) +
                20 * math.sin(self.t * 0.03 + i * 0.5) +
                10 * math.cos(self.t * 0.025 + i * 0.3)
            )
            
            y_movement = (
                sphere['offset_y'] * math.cos(self.t * 0.02 * sphere['freq_y'] + sphere['phase_y']) +
                15 * math.cos(self.t * 0.035 + i * 0.7) +
                8 * math.sin(self.t * 0.028 + i * 0.4)
            )
            
            sphere['current_x'] = sphere['base_x'] + x_movement
            sphere['current_y'] = sphere['base_y'] + y_movement
            
            # Update radius with breathing effect
            sphere['current_radius'] = sphere['radius'] + 5 * math.sin(self.t * 0.04 + i * 0.6)
    
    def draw_frame(self):
        """Draw one frame of the animation"""
        self.canvas.delete("all")
        
        # Update positions
        self.update_positions()
        
        # Draw connections first (behind spheres)
        for i in range(len(self.spheres)):
            for j in range(i + 1, len(self.spheres)):
                self.draw_connection(self.spheres[i], self.spheres[j])
        
        # Draw spheres
        for i, sphere in enumerate(self.spheres):
            x = sphere['current_x']
            y = sphere['current_y']
            radius = sphere['current_radius']
            
            # Calculate color that shifts over time
            hue = (sphere['hue_offset'] + self.t * 0.01) % 1.0
            
            self.create_gradient_circle(x, y, radius, hue)
        
        # Add title
        self.canvas.create_text(400, 30, 
                               text="Flowing Connected Spheres", 
                               fill='white', font=('Arial', 16, 'bold'))
        
        self.canvas.create_text(400, 50, 
                               text="Organic movement with gradient colors", 
                               fill='cyan', font=('Arial', 10))
    
    def animate(self):
        """Main animation loop"""
        self.draw_frame()
        self.t += 1
        
        # Schedule next frame (60 FPS)
        self.root.after(16, self.animate)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Create and run the flowing spheres animation
if __name__ == "__main__":
    app = FlowingSpheres()
    app.run()
