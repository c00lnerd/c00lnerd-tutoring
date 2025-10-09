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
        self.persistent_trails = False  # Toggle for persistent vs fading trails
        
        # Control variables
        self.speed_var = tk.DoubleVar(value=1.0)  # Animation speed multiplier
        self.trail_var = tk.IntVar(value=1000)    # Trail length control
        self.pattern_var = tk.IntVar(value=1)     # Pattern selection
        
        # 3D visualization parameters
        self.rotation_x = 0
        self.rotation_y = 0
        self.pan_x = 0  # Horizontal panning offset
        self.pan_y = 0  # Vertical panning offset
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
        
        # Mouse event bindings for 3D rotation and zoom
        self.canvas.bind("<Button-1>", self.mouse_down_event)
        self.canvas.bind("<B1-Motion>", self.mouse_drag_event)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up_event)
        self.canvas.bind("<MouseWheel>", self.mouse_wheel_event)
        self.canvas.focus_set()  # Allow canvas to receive mouse wheel events
        
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
        speed_scale = tk.Scale(control_frame, from_=0.1, to=3.0, resolution=0.1, 
                              orient=tk.HORIZONTAL, variable=self.speed_var,
                              bg='#2C3E50', fg='white', highlightthickness=0)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Pattern selection
        tk.Label(control_frame, text="Pattern:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=10)
        for i in range(1, 7):  # Now 6 patterns
            tk.Radiobutton(control_frame, text=f"{i}", variable=self.pattern_var, 
                          value=i, bg='#2C3E50', fg='white', 
                          selectcolor='#3498DB').pack(side=tk.LEFT)
        
        # 3D controls
        tk.Label(control_frame, text="3D View:", bg='#2C3E50', fg='white').pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="🔄 Reset View", 
                 command=self.reset_view, bg='#9B59B6', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Persistent trails toggle
        tk.Button(control_frame, text="🎨 Toggle Persistent", 
                 command=self.toggle_persistent_trails, bg='#E67E22', fg='white').pack(side=tk.LEFT, padx=5)
        
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
        """Handle mouse drag for 3D rotation or panning"""
        if self.mouse_down:
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            
            # Check if Shift key is held down for panning
            # Use more specific Shift key detection
            if event.state & 0x0001:  # Shift key modifier (more specific)
                # Pan the view
                self.pan_x += dx
                self.pan_y += dy
            else:
                # Rotate the view
                self.rotation_y += dx * 0.01  # Horizontal movement rotates around Y-axis
                self.rotation_x += dy * 0.01  # Vertical movement rotates around X-axis
            
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
    
    def mouse_up_event(self, event):
        """Handle mouse release"""
        self.mouse_down = False
    
    def mouse_wheel_event(self, event):
        """Handle mouse wheel for zooming"""
        # Zoom factor based on wheel direction
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        
        # Adjust focal length for zoom effect
        self.focal_length *= zoom_factor
        
        # Keep focal length within reasonable bounds
        self.focal_length = max(100, min(1000, self.focal_length))
    
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
    
    def rotate_3d_point(self, x, y, z):
        """Apply 3D rotations to a point (object rotation, not camera rotation)"""
        # Invert rotation angles for object rotation (opposite of camera rotation)
        rot_y = -self.rotation_y  # Invert Y rotation
        rot_x = -self.rotation_x  # Invert X rotation
        
        # Rotate around Y-axis first (horizontal mouse movement)
        x_rot = x * math.cos(rot_y) - z * math.sin(rot_y)
        z_rot = x * math.sin(rot_y) + z * math.cos(rot_y)
        
        # Then rotate around X-axis (vertical mouse movement)
        y_rot = y * math.cos(rot_x) - z_rot * math.sin(rot_x)
        z_final = y * math.sin(rot_x) + z_rot * math.cos(rot_x)
        
        return x_rot, y_rot, z_final
    
    def project_to_2d(self, x, y, z):
        """Project 3D coordinates to 2D screen coordinates"""
        # Perspective projection (no rotation here - rotation applied to points directly)
        if z > -50:  # Prevent division by zero/negative
            z = -50
        
        screen_x = 450 + (x * self.focal_length) / (-z) + self.pan_x
        screen_y = 300 + (y * self.focal_length) / (-z) + self.pan_y
        
        return screen_x, screen_y, z
    
    def flower_pattern_3d(self, t):
        """Create 6 completely independent 3D mathematical objects"""
        points = []
        
        # Object 1: True 3D Rose using spherical coordinates
        # ρ(θ,φ) = a * cos(m*θ) * (cos(n*φ))^k
        # Then convert to Cartesian: x = ρ*cos(θ)*cos(φ), y = ρ*sin(θ)*cos(φ), z = ρ*sin(φ)
        theta = t * 2  # Azimuthal angle
        phi = t * 1.5  # Polar angle
        a = 80  # Scale factor
        m = 4   # Rose petals parameter
        n = 3   # Polar variation parameter
        k = 2   # Power parameter
        
        rho = a * math.cos(m * theta) * (math.cos(n * phi) ** k)
        x1 = rho * math.cos(theta) * math.cos(phi)
        y1 = rho * math.sin(theta) * math.cos(phi)
        z1 = self.z_offset + rho * math.sin(phi)
        points.append((x1, y1, z1, 0))
        
        # Object 2: Lissajous Curve with Z-twist
        x2 = 80 * math.sin(2*t + 1)
        y2 = 70 * math.sin(3*t + 2)
        z2 = self.z_offset + 60 * math.cos(t * 0.8)
        points.append((x2, y2, z2, 1))
        
        # Object 3: Spiral with varying radius
        radius3 = 50 + 30 * math.sin(t * 0.5)
        x3 = radius3 * math.cos(t * 1.7)
        y3 = radius3 * math.sin(t * 1.7)
        z3 = self.z_offset + t * 2 % 120 - 60
        points.append((x3, y3, z3, 2))
        
        # Object 4: Figure-8 with 3D rotation
        x4 = 90 * math.sin(t * 1.3)
        y4 = 45 * math.sin(2 * t * 1.3)
        z4 = self.z_offset + 50 * math.cos(t * 1.1)
        points.append((x4, y4, z4, 3))
        
        # Object 5: Epicycloid (wheel rolling around circle)
        R, r = 40, 15
        x5 = (R + r) * math.cos(t * 0.9) - r * math.cos((R + r) / r * t * 0.9)
        y5 = (R + r) * math.sin(t * 0.9) - r * math.sin((R + r) / r * t * 0.9)
        z5 = self.z_offset + 35 * math.sin(t * 2.1)
        points.append((x5, y5, z5, 4))
        
        # Object 6: Butterfly curve in 3D
        x6 = 70 * math.sin(t * 1.4) * (math.exp(math.cos(t * 1.4)) - 2 * math.cos(4 * t * 1.4) - math.sin(t * 1.4 / 12)**5)
        y6 = 70 * math.cos(t * 1.4) * (math.exp(math.cos(t * 1.4)) - 2 * math.cos(4 * t * 1.4) - math.sin(t * 1.4 / 12)**5)
        z6 = self.z_offset + 45 * math.sin(t * 1.6)
        points.append((x6 * 0.3, y6 * 0.3, z6, 5))  # Scale down butterfly
        
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
    
    def single_lissajous_3d(self, t):
        """Create a single 3D Lissajous curve centered at origin for rotation testing"""
        points = []
        
        # Single Lissajous curve centered at screen center (0,0,z_offset)
        # This will help test if rotation center is correct
        x = 100 * math.sin(2 * t)      # X frequency = 2
        y = 80 * math.sin(3 * t)       # Y frequency = 3  
        z = self.z_offset + 60 * math.sin(t * 0.7)  # Gentle Z oscillation
        
        points.append((x, y, z, 0))  # Single object, trail ID 0
        
        return points
    
    def single_3d_rose(self, t):
        """Create a single 3D rose using spherical coordinates for clear viewing"""
        points = []
        
        # Smooth 3D Rose using spherical coordinates with gentle parameters
        # ρ(θ,φ) = a * cos(m*θ) * (cos(n*φ))^k
        # Convert to Cartesian: x = ρ*cos(θ)*cos(φ), y = ρ*sin(θ)*cos(φ), z = ρ*sin(φ)
        theta = t * 1.2  # Slower azimuthal angle for smoother curves
        phi = t * 0.8    # Slower polar angle for gentler 3D variation
        a = 100          # Scale factor
        m = 3            # Fewer petals for smoother appearance
        n = 2            # Simpler polar variation
        k = 0.8          # Lower power for smoother transitions
        
        # Use natural cosine function for authentic 3D rose shape
        rho = a * (0.5 + 0.5 * math.cos(m * theta)) * (0.7 + 0.3 * math.cos(n * phi)) ** k
        x = rho * math.cos(theta) * math.cos(phi)
        y = rho * math.sin(theta) * math.cos(phi)
        z = self.z_offset + rho * math.sin(phi)
        
        points.append((x, y, z, 0))  # Single 3D rose, trail ID 0
        
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
        elif pattern == 4:
            return self.dna_helix_pattern_3d(t)
        elif pattern == 5:
            return self.single_lissajous_3d(t)
        else:  # pattern == 6
            return self.single_3d_rose(t)
    
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
                
                
                # Limit trail length only if not persistent
                if not self.persistent_trails and len(self.trails[trail_id]) > self.trail_length:
                    self.trails[trail_id].pop(0)
        
        # Clear canvas and redraw trails
        self.canvas.delete("all")
        
        # Draw trails with enhanced colors and 3D rotation
        for trail_id, trail in enumerate(self.trails):
            if len(trail) > 1:
                base_color = self.colors[trail_id % len(self.colors)]
                
                # Convert trail points from 3D to 2D in real-time (so they rotate!)
                projected_trail = []
                
                # Use fixed mathematical center for each pattern (not dynamic trail center)
                # This prevents the rotation center from drifting as trails grow
                center_x = 0  # All patterns are mathematically centered at origin
                center_y = 0
                center_z = self.z_offset  # Use the same Z offset as the patterns
                
                for x3d, y3d, z3d in trail:
                    # Translate to origin (relative to object center)
                    rel_x = x3d - center_x
                    rel_y = y3d - center_y
                    rel_z = z3d - center_z
                    
                    # Apply rotation around object center
                    x_rot, y_rot, z_rot = self.rotate_3d_point(rel_x, rel_y, rel_z)
                    
                    # Translate back to world coordinates
                    final_x = x_rot + center_x
                    final_y = y_rot + center_y
                    final_z = z_rot + center_z
                    
                    # Then project to 2D
                    screen_x, screen_y, depth = self.project_to_2d(final_x, final_y, final_z)
                    projected_trail.append((screen_x, screen_y, depth))
                
                # Draw the trail with beautiful color gradients
                for i in range(1, len(projected_trail)):
                    prev_x, prev_y, prev_depth = projected_trail[i-1]
                    curr_x, curr_y, curr_depth = projected_trail[i]
                    
                    # Check if the line segment is too long (indicates a jump/discontinuity)
                    line_length = math.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
                    max_line_length = 150  # Skip drawing lines longer than this
                    
                    if line_length > max_line_length:
                        continue  # Skip this line segment - it's a jump in space
                    
                    # Depth-based sizing
                    avg_depth = (prev_depth + curr_depth) / 2
                    depth_factor = max(0.2, min(1.0, (-avg_depth - 200) / 400))
                    
                    if self.persistent_trails:
                        # Persistent trails: all segments are bright and colorful
                        line_color = base_color
                        width = max(1, int(2 * depth_factor))  # Ensure minimum width of 1
                    else:
                        # Fading trails: create gradient effect
                        alpha = i / len(projected_trail)
                        
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
            # Apply same rotation as trail points for consistency
            center_x = 0
            center_y = 0  
            center_z = self.z_offset
            
            # Translate to origin, rotate, translate back (same as trail rendering)
            rel_x = x - center_x
            rel_y = y - center_y
            rel_z = z - center_z
            
            x_rot, y_rot, z_rot = self.rotate_3d_point(rel_x, rel_y, rel_z)
            
            final_x = x_rot + center_x
            final_y = y_rot + center_y
            final_z = z_rot + center_z
            
            screen_x, screen_y, depth = self.project_to_2d(final_x, final_y, final_z)
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
        
        # Draw 3D axis indicator in bottom-right corner
        self.draw_3d_axis_indicator()
        
        # Draw instructions
        self.canvas.create_text(450, 20, text="🖱️ Drag: rotate | ⇧+Drag: pan | 🖱️ Wheel: zoom", 
                               fill='white', font=('Arial', 12))
        zoom_level = self.focal_length / 500.0  # 500 is default focal length
        trail_mode = "Persistent" if self.persistent_trails else f"{self.trail_length}"
        self.canvas.create_text(450, 580, 
                               text=f"Pattern {self.pattern_var.get()} | Trail: {trail_mode} | Speed: {self.speed_var.get():.1f}x | Zoom: {zoom_level:.1f}x", 
                               fill='cyan', font=('Arial', 10))
    
    def draw_3d_axis_indicator(self):
        """Draw a small 3D coordinate system in the bottom-right corner"""
        # Position in bottom-right corner
        center_x, center_y = 850, 550
        axis_length = 40
        
        # Define 3D axis vectors
        axes = [
            (axis_length, 0, 0, '#FF4444', 'X'),  # Red X-axis
            (0, axis_length, 0, '#44FF44', 'Y'),  # Green Y-axis  
            (0, 0, axis_length, '#4444FF', 'Z')   # Blue Z-axis
        ]
        
        # Draw background circle
        self.canvas.create_oval(center_x-45, center_y-45, center_x+45, center_y+45, 
                               fill='#000000', outline='#333333', width=1)
        
        # Draw each axis
        for ax, ay, az, color, label in axes:
            # Apply same rotation as main objects
            x_rot, y_rot, z_rot = self.rotate_3d_point(ax, ay, az)
            
            # Convert to screen coordinates (no perspective, just orthographic)
            end_x = center_x + x_rot
            end_y = center_y + y_rot
            
            # Draw axis line with thickness based on depth
            depth_factor = max(0.3, (z_rot + axis_length) / (2 * axis_length))
            line_width = max(1, int(3 * depth_factor))
            
            # Draw the axis line
            self.canvas.create_line(center_x, center_y, end_x, end_y, 
                                   fill=color, width=line_width, capstyle=tk.ROUND)
            
            # Draw arrowhead
            if depth_factor > 0.5:  # Only draw arrow if pointing towards viewer
                # Calculate arrow direction
                dx = end_x - center_x
                dy = end_y - center_y
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Normalize
                    dx /= length
                    dy /= length
                    
                    # Arrow points
                    arrow_size = 8 * depth_factor
                    arrow_x1 = end_x - arrow_size * dx - arrow_size * 0.3 * dy
                    arrow_y1 = end_y - arrow_size * dy + arrow_size * 0.3 * dx
                    arrow_x2 = end_x - arrow_size * dx + arrow_size * 0.3 * dy
                    arrow_y2 = end_y - arrow_size * dy - arrow_size * 0.3 * dx
                    
                    # Draw arrowhead
                    self.canvas.create_polygon(end_x, end_y, arrow_x1, arrow_y1, arrow_x2, arrow_y2,
                                             fill=color, outline=color)
            
            # Draw axis label
            label_x = center_x + x_rot * 1.3
            label_y = center_y + y_rot * 1.3
            self.canvas.create_text(label_x, label_y, text=label, fill=color, 
                                   font=('Arial', 10, 'bold'))
        
        # Draw center dot
        self.canvas.create_oval(center_x-2, center_y-2, center_x+2, center_y+2, 
                               fill='white', outline='white')
    
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
        """Reset 3D view, zoom, and panning to default"""
        self.rotation_x = 0
        self.rotation_y = 0
        self.pan_x = 0
        self.pan_y = 0
        self.focal_length = 500  # Reset zoom to default
    
    def toggle_persistent_trails(self):
        """Toggle between persistent and fading trails"""
        self.persistent_trails = not self.persistent_trails
        if not self.persistent_trails:
            # When switching back to fading trails, trim existing trails to normal length
            for trail in self.trails:
                while len(trail) > self.trail_length:
                    trail.pop(0)
    
    def run(self):
        """Start the application"""
        print("🎨 3D Parametric Mathematical Art")
        print("Controls:")
        print("• 🖱️ Click and drag: Rotate 3D view")
        print("• ⇧+Drag: Pan (move) the view")
        print("• 🖱️ Mouse wheel: Zoom in/out")
        print("• ⏯️ Pause/Resume: Toggle animation")
        print("• 🗑️ Clear: Clear all trails")
        print("• 🔄 Reset: Start over from beginning")
        print("• 🔄 Reset View: Return to default 3D view and zoom")
        print("• 🎨 Toggle Persistent: Switch between fading and permanent trails")
        print("• Speed slider: Adjust animation speed")
        print("• Pattern buttons: Switch between different 3D patterns")
        print("• Trail slider: Adjust trail length (200-2000 points)")
        print("\nPattern Types:")
        print("1. Independent Objects: Rose, Lissajous, Spiral, Figure-8, Epicycloid, Butterfly")
        print("2. 3D Spirograph: Classic geometric curves with depth")
        print("3. 3D Lissajous: Modulated harmonic motion in three dimensions")
        print("4. DNA Helix: Double helix with connecting bridges")
        print("5. Single Lissajous: One centered object for testing rotation center")
        print("6. Pure 3D Rose: Single spherical coordinate rose for clear viewing")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ParametricArt3D()
    app.run()
