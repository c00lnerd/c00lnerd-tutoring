import tkinter as tk
import math
import time

class ParametricArt:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parametric Mathematical Art")
        self.root.geometry("800x600")
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        # Animation parameters
        self.t = 0
        self.dt = 0.1
        self.running = True
        
        # Colors for the patterns
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Pause/Resume", command=self.toggle_pause).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        
        # Speed control
        tk.Label(button_frame, text="Speed:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(button_frame, from_=0.1, to=3.0, resolution=0.1, 
                              orient=tk.HORIZONTAL, variable=self.speed_var)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        self.animate()
    
    def parametric_function(self, t, k):
        """
        Recreates the JavaScript parametric equations:
        a = (x, y, d=5*cos(o=mag(k=x/8-25, e=y/8-25)/3))
        """
        # Center the coordinates around the canvas center
        center_x, center_y = 400, 300
        
        # Multiple overlapping patterns for complexity
        patterns = []
        
        for i in range(3):  # Create 3 overlapping patterns
            # Adjust the mathematical parameters for different patterns
            scale = 50 + i * 30
            freq1 = 2 + i * 0.5
            freq2 = 3 + i * 0.7
            phase = i * math.pi / 3
            
            # Complex parametric equations similar to the JavaScript version
            x = center_x + scale * math.cos(freq1 * t + phase) * math.sin(freq2 * t)
            y = center_y + scale * math.sin(freq1 * t + phase) * math.cos(freq2 * t * 0.8)
            
            # Add some mathematical complexity
            x += 20 * math.cos(t * 5 + i) * math.sin(t * 2)
            y += 20 * math.sin(t * 4 + i) * math.cos(t * 3)
            
            patterns.append((x, y, i))
        
        return patterns
    
    def draw_frame(self):
        """Draw one frame of the animation"""
        # Get points for current time
        points = self.parametric_function(self.t, 0)
        
        # Draw each pattern
        for i, (x, y, pattern_id) in enumerate(points):
            color = self.colors[pattern_id % len(self.colors)]
            
            # Draw a small circle at each point
            radius = 2
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                  fill=color, outline=color)
            
            # Connect to previous points for flowing lines
            if hasattr(self, 'prev_points') and len(self.prev_points) > pattern_id:
                prev_x, prev_y = self.prev_points[pattern_id]
                self.canvas.create_line(prev_x, prev_y, x, y, fill=color, width=1)
        
        # Store current points for next frame
        self.prev_points = [(x, y) for x, y, _ in points]
    
    def animate(self):
        """Main animation loop"""
        if self.running:
            self.draw_frame()
            self.t += self.dt * self.speed_var.get()
        
        # Schedule next frame
        self.root.after(50, self.animate)  # ~20 FPS
    
    def toggle_pause(self):
        """Toggle animation pause"""
        self.running = not self.running
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
    
    def reset(self):
        """Reset animation to beginning"""
        self.t = 0
        self.clear_canvas()
        if hasattr(self, 'prev_points'):
            del self.prev_points
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Alternative version with more complex mathematical patterns
class AdvancedParametricArt:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Parametric Mathematical Art")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        self.t = 0
        self.running = True
        self.trail_length = 500  # Number of points to keep in trail
        self.trails = [[] for _ in range(5)]  # Multiple trails
        
        # Controls
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Pause/Resume", command=self.toggle_pause).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        
        # Pattern selector
        tk.Label(button_frame, text="Pattern:").pack(side=tk.LEFT, padx=5)
        self.pattern_var = tk.IntVar(value=1)
        for i in range(1, 4):
            tk.Radiobutton(button_frame, text=f"Pattern {i}", variable=self.pattern_var, 
                          value=i).pack(side=tk.LEFT)
        
        self.animate()
    
    def complex_parametric(self, t, pattern_type):
        """More complex parametric equations"""
        center_x, center_y = 400, 300
        points = []
        
        if pattern_type == 1:
            # Flower-like pattern (similar to your JavaScript)
            for i in range(5):
                a = i * 2 * math.pi / 5
                r = 100 + 50 * math.cos(5 * t + a)
                x = center_x + r * math.cos(t * 2 + a) * math.cos(t * 0.5)
                y = center_y + r * math.sin(t * 2 + a) * math.sin(t * 0.7)
                points.append((x, y, i))
        
        elif pattern_type == 2:
            # Spirograph-like pattern
            for i in range(3):
                R = 80 + i * 20  # Outer circle radius
                r = 30 + i * 10  # Inner circle radius
                d = 40 + i * 15  # Distance from inner circle center
                
                angle = t * (1 + i * 0.3)
                x = center_x + (R - r) * math.cos(angle) + d * math.cos((R - r) / r * angle)
                y = center_y + (R - r) * math.sin(angle) - d * math.sin((R - r) / r * angle)
                points.append((x, y, i))
        
        elif pattern_type == 3:
            # Lissajous curves with modulation
            for i in range(4):
                a = 3 + i * 0.5
                b = 2 + i * 0.3
                phase = i * math.pi / 4
                
                x = center_x + 150 * math.cos(a * t + phase) * (1 + 0.3 * math.sin(t * 0.5))
                y = center_y + 150 * math.sin(b * t + phase) * (1 + 0.3 * math.cos(t * 0.7))
                points.append((x, y, i))
        
        return points
    
    def draw_advanced_frame(self):
        """Draw frame with trailing effect"""
        points = self.complex_parametric(self.t, self.pattern_var.get())
        
        # Add new points to trails
        for i, (x, y, trail_id) in enumerate(points):
            if trail_id < len(self.trails):
                self.trails[trail_id].append((x, y))
                
                # Limit trail length
                if len(self.trails[trail_id]) > self.trail_length:
                    self.trails[trail_id].pop(0)
        
        # Clear and redraw all trails
        self.canvas.delete("all")
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for trail_id, trail in enumerate(self.trails):
            if len(trail) > 1:
                color = colors[trail_id % len(colors)]
                
                # Draw trail with fading effect
                for i in range(1, len(trail)):
                    alpha = i / len(trail)  # Fade effect
                    prev_x, prev_y = trail[i-1]
                    curr_x, curr_y = trail[i]
                    
                    # Simulate alpha by using lighter colors for older points
                    if alpha > 0.7:
                        line_color = color
                        width = 2
                    elif alpha > 0.4:
                        line_color = '#666666'
                        width = 1
                    else:
                        line_color = '#333333'
                        width = 1
                    
                    self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, 
                                          fill=line_color, width=width)
    
    def animate(self):
        if self.running:
            self.draw_advanced_frame()
            self.t += 0.05
        
        self.root.after(30, self.animate)
        self.trails = [[] for _ in range(5)]
        
        # 3D visualization parameters
        self.rotation_x = 0
        self.rotation_y = 0
        self.mouse_down = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.focal_length = 400
        self.z_offset = -200  # Move patterns back in 3D space
    
    def reset(self):
        self.t = 0
        self.clear_canvas()
        self.root.mainloop()

if __name__ == "__main__":
    print("Choose your parametric art experience:")
    print("1. Simple Parametric Art")
    print("2. Advanced Parametric Art with Trails")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        app = AdvancedParametricArt()
    else:
        app = ParametricArt()
    
    app.run()
