import tkinter as tk
import math
import time

class ParametricArt3D:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D Parametric Mathematical Art")
        self.root.geometry("900x700")
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=900, height=600, bg='black')
        self.canvas.pack()
        
        # Animation parameters
        self.t = 0
        self.dt = 0.05
        self.running = True
        self.trail_length = 1000  # Very long trails for beautiful effects
        self.trails = [[] for _ in range(6)]  # 6 different pattern elements
        
        # 3D visualization parameters
        self.rotation_x = 0
        self.rotation_y = 0
        self.mouse_down = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.focal_length = 500
        self.z_offset = -300  # Move patterns back in 3D space
        
        # Enhanced colors for beautiful trails
        self.colors = [
            '#FF6B6B',  # Coral Red
            '#4ECDC4',  # Turquoise
            '#45B7D1',  # Sky Blue
            '#96CEB4',  # Mint Green
            '#FFEAA7',  # Warm Yellow
            '#DDA0DD',  # Plum
            '#FF9F43',  # Orange
            '#00D2D3',  # Cyan
            '#FF7675',  # Light Red
            '#74B9FF',  # Bright Blue
            '#00B894',  # Emerald
            '#FDCB6E'   # Golden Yellow
        ]
        
        # Mouse event bindings for 3D rotation
        self.canvas.bind("<Button-1>", self.mouse_down_event)
        self.canvas.bind("<B1-Motion>", self.mouse_drag_event)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up_event)
        
        # Create control panel
        self.create_controls()
        
        # Start animation
        self.animate()
    
    def create_controls(self):
        """Create the control panel"""
        control_frame = tk.Frame(self.root, bg='#2C3E50')
        control_frame.pack(fill=tk.X, pady=5)
        
        # Animation controls
        tk.Button(control_frame, text="⏯️ Pause/Resume", 
                 command=self.toggle_pause, bg='#3498DB', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🗑️ Clear", 
                 command=self.clear_canvas, bg='#E74C3C', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🔄 Reset", 
                 command=self.reset, bg='#27AE60', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Speed control
        tk.Label(control_frame, text="Speed:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(control_frame, from_=0.1, to=3.0, resolution=0.1, 
                              orient=tk.HORIZONTAL, variable=self.speed_var,
                              bg='#2C3E50', fg='white', highlightthickness=0)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Pattern selector
        tk.Label(control_frame, text="Pattern:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=5)
        self.pattern_var = tk.IntVar(value=1)
        for i in range(1, 5):
            tk.Radiobutton(control_frame, text=f"{i}", variable=self.pattern_var, 
                          value=i, bg='#2C3E50', fg='white', 
                          selectcolor='#3498DB').pack(side=tk.LEFT)
        
        # 3D controls
        tk.Label(control_frame, text="3D View:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="🔄 Reset View", 
                 command=self.reset_view, bg='#9B59B6', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Trail length control
        tk.Label(control_frame, text="Trail:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=5)
        self.trail_var = tk.IntVar(value=1000)
        trail_scale = tk.Scale(control_frame, from_=200, to=2000, resolution=100, 
                              orient=tk.HORIZONTAL, variable=self.trail_var,
                              bg='#2C3E50', fg='white', highlightthickness=0)
        trail_scale.pack(side=tk.LEFT, padx=5)
    
    def mouse_down_event(self, event):
        """Handle mouse press for 3D rotation"""
        self.mouse_down = True
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
    
    def mouse_drag_event(self, event):
        """Handle mouse drag for 3D rotation"""
        if self.mouse_down:
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            
            # Update rotation based on mouse movement
            self.rotation_y += dx * 0.01  # Horizontal movement rotates around Y-axis
            self.rotation_x += dy * 0.01  # Vertical movement rotates around X-axis
            
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
    
    def mouse_up_event(self, event):
        """Handle mouse release"""
        self.mouse_down = False
    
    def _blend_color(self, color1, color2, blend_factor):
        """Blend two hex colors together"""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        # Blend the colors
        blended = tuple(rgb1[i] * (1 - blend_factor) + rgb2[i] * blend_factor for i in range(3))
        return rgb_to_hex(blended)
    
    def project_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates with rotation"""
        # Apply 3D rotations
        # Rotate around X-axis
        y_rot = y * math.cos(self.rotation_x) - z * math.sin(self.rotation_x)
        z_rot = y * math.sin(self.rotation_x) + z * math.cos(self.rotation_x)
        
        # Rotate around Y-axis
        x_rot = x * math.cos(self.rotation_y) + z_rot * math.sin(self.rotation_y)
        z_final = -x * math.sin(self.rotation_y) + z_rot * math.cos(self.rotation_y)
        
        # Perspective projection
        if z_final > -50:  # Prevent division by zero/negative
            z_final = -50
        
        screen_x = 450 + (x_rot * self.focal_length) / (-z_final)
        screen_y = 300 + (y_rot * self.focal_length) / (-z_final)
        
        return screen_x, screen_y, z_final
    
    def flower_pattern_3d(self, t):
        """Create 3D flowing flower-like patterns"""
        points = []
        
        for i in range(6):
            # Each element has different phase and frequency
            phase = i * 2 * math.pi / 6
            
            # 3D parametric equations for organic flow
            base_radius = 80 + 30 * math.cos(3 * t + phase)
            
            # X and Y create the flower pattern
            x = base_radius * math.cos(2 * t + phase) * (1 + 0.3 * math.sin(t * 0.5))
            y = base_radius * math.sin(2 * t + phase) * (1 + 0.3 * math.cos(t * 0.7))
            
            # Z creates depth variation
            z = self.z_offset + 50 * math.sin(t * 1.5 + phase) + 20 * math.cos(t * 2 + i)
            
            # Add subtle secondary motion in all dimensions
            x += 15 * math.cos(5 * t + i)
            y += 15 * math.sin(4 * t + i)
            z += 10 * math.sin(3 * t + phase)
            
            points.append((x, y, z, i))
        
        return points
    
    def spirograph_pattern_3d(self, t):
        """Create 3D spirograph-like patterns"""
        points = []
        
        for i in range(4):
            # Spirograph parameters
            R = 100 + i * 25  # Outer circle radius
            r = 20 + i * 8    # Inner circle radius  
            d = 40 + i * 15   # Distance from inner circle center
            
            # Spirograph equations
            ratio = (R - r) / r
            angle = t * (1 + i * 0.2)
            
            x = (R - r) * math.cos(angle) + d * math.cos(ratio * angle)
            y = (R - r) * math.sin(angle) - d * math.sin(ratio * angle)
            
            # Add 3D depth with helical motion
            z = self.z_offset + 60 * math.sin(t * 0.8 + i * math.pi/2) + 30 * math.cos(angle * 0.1)
            
            points.append((x, y, z, i))
        
        return points
    
    def lissajous_pattern_3d(self, t):
        """Create 3D modulated Lissajous curves"""
        points = []
        
        for i in range(5):
            # Lissajous parameters
            a = 3 + i * 0.4
            b = 2 + i * 0.3
            c = 1.5 + i * 0.2  # Z frequency
            phase = i * math.pi / 5
            
            # 3D Lissajous equations
            amplitude = 100 * (1 + 0.4 * math.sin(t * 0.3 + i))
            x = amplitude * math.cos(a * t + phase)
            y = amplitude * math.sin(b * t + phase)
            z = self.z_offset + 80 * math.sin(c * t + phase * 2)
            
            points.append((x, y, z, i))
        
        return points
    
    def dna_helix_pattern_3d(self, t):
        """Create DNA double helix pattern"""
        points = []
        
        for i in range(2):  # Two helices
            for j in range(3):  # Multiple points per helix
                angle = t * 2 + i * math.pi + j * math.pi / 3
                
                # Helix parameters
                radius = 60 + 20 * math.sin(t * 0.5)
                height_speed = 30
                
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                z = self.z_offset + height_speed * (t + j * 0.5) % 200 - 100
                
                # Add connecting bridges occasionally
                if j == 1 and math.sin(t * 3) > 0.8:
                    # Bridge point
                    x *= 0.5
                    y *= 0.5
                
                points.append((x, y, z, i * 3 + j))
        
        return points
    
    def get_pattern_points_3d(self, t):
        """Get 3D points based on selected pattern"""
        pattern = self.pattern_var.get()
        
        if pattern == 1:
            return self.flower_pattern_3d(t)
        elif pattern == 2:
            return self.spirograph_pattern_3d(t)
        elif pattern == 3:
            return self.lissajous_pattern_3d(t)
        else:
            return self.dna_helix_pattern_3d(t)
    
    def draw_frame_3d(self):
        """Draw one frame of 3D animation with trailing effects"""
        # Update trail length from slider
        self.trail_length = self.trail_var.get()
        
        points_3d = self.get_pattern_points_3d(self.t)
        
        # Store 3D points in trails (so they rotate with view changes)
        for i, (x, y, z, trail_id) in enumerate(points_3d):
            if trail_id < len(self.trails):
                # Store 3D coordinates, not 2D screen coordinates
                self.trails[trail_id].append((x, y, z))
                
                # Limit trail length
                if len(self.trails[trail_id]) > self.trail_length:
                    self.trails[trail_id].pop(0)
        
        # Clear canvas and redraw trails
        self.canvas.delete("all")
        
        # Draw trails with enhanced colors and 3D rotation
        for trail_id, trail in enumerate(self.trails):
            if len(trail) > 1:
                base_color = self.colors[trail_id % len(self.colors)]
                
                # Convert trail points from 3D to 2D in real-time (so they rotate!)
                projected_trail = []
                for x3d, y3d, z3d in trail:
                    screen_x, screen_y, depth = self.project_to_2d(x3d, y3d, z3d)
                    projected_trail.append((screen_x, screen_y, depth))
                
                # Draw the trail with beautiful color gradients
                for i in range(1, len(projected_trail)):
                    # Create fading and depth effects
                    alpha = i / len(projected_trail)
                    prev_x, prev_y, prev_depth = projected_trail[i-1]
                    curr_x, curr_y, curr_depth = projected_trail[i]
                    
                    # Depth-based sizing and enhanced coloring
                    avg_depth = (prev_depth + curr_depth) / 2
                    depth_factor = max(0.2, min(1.0, (-avg_depth - 200) / 400))
                    
                    # Enhanced color system with gradients
                    if alpha > 0.9:  # Newest parts - brightest
                        line_color = base_color
                        width = int(4 * depth_factor)
                    elif alpha > 0.7:  # Recent parts - bright
                        line_color = self._blend_color(base_color, '#FFFFFF', 0.3)
                        width = int(3 * depth_factor)
                    elif alpha > 0.4:  # Middle parts - medium
                        line_color = self._blend_color(base_color, '#888888', 0.5)
                        width = int(2 * depth_factor)
                    elif alpha > 0.2:  # Older parts - dim
                        line_color = self._blend_color(base_color, '#444444', 0.7)
                        width = max(1, int(1 * depth_factor))
                    else:  # Oldest parts - very dim
                        line_color = '#222222'
                        width = 1
                    
                    if width > 0 and prev_x > 0 and curr_x > 0:  # Only draw visible points
                        self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, 
                                              fill=line_color, width=width, 
                                              capstyle=tk.ROUND, smooth=True)
        
        # Draw current points as bright, glowing dots with depth sizing
        for x, y, z, trail_id in points_3d:
            screen_x, screen_y, depth = self.project_to_2d(x, y, z)
            base_color = self.colors[trail_id % len(self.colors)]
            
            # Size based on depth
            depth_factor = max(0.3, min(1.0, (-depth - 200) / 300))
            radius = int(5 * depth_factor)
            
            if radius > 0 and screen_x > 0 and screen_y > 0:
                # Create glowing effect with multiple circles
                # Outer glow
                glow_color = self._blend_color(base_color, '#FFFFFF', 0.7)
                self.canvas.create_oval(screen_x-radius-1, screen_y-radius-1, 
                                      screen_x+radius+1, screen_y+radius+1, 
                                      fill=glow_color, outline='', width=0)
                
                # Main dot
                self.canvas.create_oval(screen_x-radius, screen_y-radius, 
                                      screen_x+radius, screen_y+radius, 
                                      fill=base_color, outline='white', width=1)
                
                # Inner highlight
                highlight_radius = max(1, radius // 2)
                self.canvas.create_oval(screen_x-highlight_radius, screen_y-highlight_radius, 
                                      screen_x+highlight_radius, screen_y+highlight_radius, 
                                      fill='white', outline='', width=0)
        
        # Draw instructions
        self.canvas.create_text(450, 20, text="🖱️ Click and drag to rotate 3D view", 
                               fill='white', font=('Arial', 12))
        self.canvas.create_text(450, 580, 
                               text=f"Pattern {self.pattern_var.get()} | Trail Length: {self.trail_length} | Speed: {self.speed_var.get():.1f}x", 
                               fill='cyan', font=('Arial', 10))
    
    def animate(self):
        """Main animation loop"""
        if self.running:
            self.draw_frame_3d()
            self.t += self.dt * self.speed_var.get()
        
        # Schedule next frame (30 FPS)
        self.root.after(33, self.animate)
    
    def toggle_pause(self):
        """Toggle animation pause"""
        self.running = not self.running
    
    def clear_canvas(self):
        """Clear the canvas and trails"""
        self.canvas.delete("all")
        self.trails = [[] for _ in range(6)]
    
    def reset(self):
        """Reset animation to beginning"""
        self.t = 0
        self.clear_canvas()
    
    def reset_view(self):
        """Reset 3D view to default"""
        self.rotation_x = 0
        self.rotation_y = 0
    
    def run(self):
        """Start the application"""
        print("🎨 3D Parametric Mathematical Art")
        print("Controls:")
        print("• 🖱️ Click and drag: Rotate 3D view")
        print("• ⏯️ Pause/Resume: Toggle animation")
        print("• 🗑️ Clear: Clear all trails")
        print("• 🔄 Reset: Start over from beginning")
        print("• 🔄 Reset View: Return to default 3D view")
        print("• Speed slider: Adjust animation speed")
        print("• Pattern buttons: Switch between different 3D patterns")
        print("• Trail slider: Adjust trail length (200-2000 points)")
        print("\nPattern Types:")
        print("1. 3D Flower Pattern: Organic flowing petals in 3D space")
        print("2. 3D Spirograph: Classic geometric curves with depth")
        print("3. 3D Lissajous: Modulated harmonic motion in three dimensions")
        print("4. DNA Helix: Double helix with connecting bridges")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ParametricArt3D()
    app.run()
