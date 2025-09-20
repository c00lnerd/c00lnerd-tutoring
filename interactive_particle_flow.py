import math
import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame
import time
import random

def create_interactive_particle_flow():
    """
    Interactive particle flow visualization with enhanced flow lines and parameter controls
    """
    root = tk.Tk()
    root.title("Interactive Particle Flow Explorer")
    root.geometry("1200x700")
    root.configure(bg='black')
    
    # Create main frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Canvas for drawing
    canvas = Canvas(main_frame, width=800, height=600, bg='black')
    canvas.pack(side=tk.LEFT, padx=(0, 20))
    
    # Control panel
    control_frame = Frame(main_frame, bg='black', width=350)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)
    control_frame.pack_propagate(False)
    
    # Title
    title_label = Label(control_frame, text="Particle Flow Controls", 
                       font=("Arial", 16, "bold"), fg="white", bg="black")
    title_label.pack(pady=(0, 20))
    
    # Parameters
    flow_strength = tk.DoubleVar(value=0.3)
    particle_count = tk.IntVar(value=50)
    particle_speed = tk.DoubleVar(value=2.0)
    trail_length = tk.IntVar(value=20)
    flow_complexity = tk.DoubleVar(value=0.02)
    center_movement = tk.DoubleVar(value=50.0)
    flow_line_density = tk.IntVar(value=24)
    flow_line_opacity = tk.DoubleVar(value=0.3)
    
    # Particle system
    particles = []
    
    class Particle:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.life = random.uniform(150, 300)
            self.max_life = self.life
            self.size = random.uniform(1, 3)
            self.trail = []
            self.hue = random.uniform(0, 360)
            
        def update(self, center_x, center_y, t, params):
            # Create flow field effect
            dx = self.x - center_x
            dy = self.y - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Create complex swirling motion
                angle = math.atan2(dy, dx)
                flow_angle = angle + math.pi/2 + math.sin(t * 0.001 + distance * params['complexity']) * 0.8
                
                # Multi-layered flow with different frequencies
                flow_angle += math.cos(t * 0.0015 + distance * params['complexity'] * 0.5) * 0.3
                flow_angle += math.sin(t * 0.002 + angle * 3) * 0.2
                
                # Flow strength with distance falloff
                flow_strength_val = max(0, 250 - distance) / 250
                flow_strength_val *= params['strength']
                
                self.vx += math.cos(flow_angle) * flow_strength_val * 0.15
                self.vy += math.sin(flow_angle) * flow_strength_val * 0.15
            
            # Add turbulence
            self.vx += random.uniform(-0.05, 0.05)
            self.vy += random.uniform(-0.05, 0.05)
            
            # Limit velocity
            max_speed = params['speed']
            speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
            if speed > max_speed:
                self.vx = (self.vx / speed) * max_speed
                self.vy = (self.vy / speed) * max_speed
            
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Add to trail
            self.trail.append((self.x, self.y))
            if len(self.trail) > params['trail_length']:
                self.trail.pop(0)
            
            # Update life
            self.life -= 1
            
            # Wrap around screen
            if self.x < 0: self.x = 800
            if self.x > 800: self.x = 0
            if self.y < 0: self.y = 600
            if self.y > 600: self.y = 0
            
        def draw(self, canvas):
            if self.life <= 0:
                return
                
            # Draw trail with enhanced colors
            for i in range(1, len(self.trail)):
                fade = (i / len(self.trail)) * (self.life / self.max_life)
                
                # Create rainbow-like colors based on particle hue
                hue_rad = math.radians(self.hue + i * 10)
                r = int(128 + 127 * math.sin(hue_rad) * fade)
                g = int(128 + 127 * math.sin(hue_rad + 2.09) * fade)  # 120 degrees
                b = int(128 + 127 * math.sin(hue_rad + 4.19) * fade)  # 240 degrees
                
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                x1, y1 = self.trail[i-1]
                x2, y2 = self.trail[i]
                
                canvas.create_line(x1, y1, x2, y2, fill=color, width=max(1, int(fade * 3)))
            
            # Draw particle
            if self.trail:
                fade = self.life / self.max_life
                size = self.size * fade
                x, y = self.trail[-1]
                
                canvas.create_oval(x-size, y-size, x+size, y+size, 
                                 fill="white", outline="cyan", width=1)
    
    def create_enhanced_flow_field(center_x, center_y, t, density, opacity):
        """Create enhanced flowing field lines"""
        field_lines = []
        
        # Create multiple layers of flow lines
        for layer in range(3):
            layer_offset = layer * 5
            for angle in range(0, 360, max(1, 360 // density)):
                points = []
                rad = math.radians(angle)
                
                # Multiple spiral patterns
                for r in range(10 + layer_offset, 350, 3):
                    # Complex flow equation with multiple harmonics
                    flow_angle = rad + r * 0.015 * (1 + layer * 0.2)
                    flow_angle += math.sin(t * 0.0008 + r * 0.008) * 0.4
                    flow_angle += math.cos(t * 0.0012 + angle * 0.1) * 0.3
                    flow_angle += math.sin(t * 0.0005 + r * 0.02 + layer) * 0.2
                    
                    x = center_x + r * math.cos(flow_angle)
                    y = center_y + r * math.sin(flow_angle)
                    
                    if 0 <= x <= 800 and 0 <= y <= 600:
                        points.append((x, y))
                    else:
                        break
                
                if len(points) > 1:
                    field_lines.append((points, layer))
        
        return field_lines
    
    def create_slider(parent, label, variable, from_, to, resolution=0.1):
        frame = Frame(parent, bg='black')
        frame.pack(fill=tk.X, pady=3)
        
        Label(frame, text=label, fg="white", bg="black", font=("Arial", 9, "bold")).pack()
        slider = Scale(frame, from_=from_, to=to, resolution=resolution, 
                      orient=tk.HORIZONTAL, variable=variable, 
                      bg="gray20", fg="white", highlightbackground="black",
                      activebackground="gray30", troughcolor="gray40")
        slider.pack(fill=tk.X)
        return slider
    
    # Flow Controls
    Label(control_frame, text="Flow Dynamics", fg="cyan", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(0, 10))
    
    create_slider(control_frame, "Flow Strength", flow_strength, 0.0, 1.0, 0.05)
    create_slider(control_frame, "Flow Complexity", flow_complexity, 0.005, 0.05, 0.005)
    create_slider(control_frame, "Center Movement", center_movement, 0, 100, 5)
    
    # Particle Controls
    Label(control_frame, text="Particle System", fg="yellow", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    create_slider(control_frame, "Max Particles", particle_count, 10, 150, 10)
    create_slider(control_frame, "Particle Speed", particle_speed, 0.5, 5.0, 0.1)
    create_slider(control_frame, "Trail Length", trail_length, 5, 50, 5)
    
    # Visual Controls
    Label(control_frame, text="Visual Effects", fg="lime", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    create_slider(control_frame, "Flow Line Density", flow_line_density, 6, 48, 6)
    create_slider(control_frame, "Flow Line Opacity", flow_line_opacity, 0.1, 1.0, 0.1)
    
    # Control buttons
    def reset_particles():
        nonlocal particles
        particles = []
    
    def reset_defaults():
        flow_strength.set(0.3)
        particle_count.set(50)
        particle_speed.set(2.0)
        trail_length.set(20)
        flow_complexity.set(0.02)
        center_movement.set(50.0)
        flow_line_density.set(24)
        flow_line_opacity.set(0.3)
        reset_particles()
    
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    reset_particles_btn = tk.Button(button_frame, text="Clear Particles", 
                                   command=reset_particles, bg="orange", fg="white", 
                                   font=("Arial", 10, "bold"), width=15)
    reset_particles_btn.pack(pady=2)
    
    reset_defaults_btn = tk.Button(button_frame, text="Reset to Defaults", 
                                  command=reset_defaults, bg="red", fg="white", 
                                  font=("Arial", 10, "bold"), width=15)
    reset_defaults_btn.pack(pady=2)
    
    # Instructions
    Label(control_frame, text="Instructions:", fg="orange", bg="black", 
          font=("Arial", 10, "bold")).pack(pady=(20, 5))
    
    instructions = [
        "• Adjust flow strength for particle attraction",
        "• Increase complexity for more turbulent flow",
        "• Higher density creates more flow lines",
        "• Experiment with different combinations",
        "• Clear particles to see immediate changes"
    ]
    
    for instruction in instructions:
        Label(control_frame, text=instruction, fg="white", bg="black", 
              font=("Arial", 8), anchor="w").pack(anchor="w", padx=10)
    
    def draw_frame():
        canvas.delete("all")
        
        current_time = time.time() * 1000
        
        # Get current parameters
        params = {
            'strength': flow_strength.get(),
            'speed': particle_speed.get(),
            'trail_length': trail_length.get(),
            'complexity': flow_complexity.get()
        }
        
        # Dynamic center point
        center_movement_val = center_movement.get()
        center_x = 400 + center_movement_val * math.sin(current_time * 0.0008)
        center_y = 300 + center_movement_val * 0.6 * math.cos(current_time * 0.0012)
        
        # Draw enhanced flow field lines
        flow_lines = create_enhanced_flow_field(center_x, center_y, current_time, 
                                               flow_line_density.get(), flow_line_opacity.get())
        
        opacity_val = flow_line_opacity.get()
        for line_data in flow_lines:
            line, layer = line_data
            if len(line) > 1:
                # Different colors for different layers
                layer_colors = [
                    (100, 150, 255),  # Blue
                    (150, 100, 255),  # Purple
                    (255, 150, 100)   # Orange
                ]
                
                base_r, base_g, base_b = layer_colors[layer % 3]
                
                for i in range(1, len(line)):
                    fade = (len(line) - i) / len(line) * opacity_val
                    
                    r = int(base_r * fade)
                    g = int(base_g * fade)
                    b = int(base_b * fade)
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    x1, y1 = line[i-1]
                    x2, y2 = line[i]
                    width = max(1, int(fade * 2))
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        
        # Particle management
        max_particles = particle_count.get()
        
        # Add new particles
        if len(particles) < max_particles and random.random() < 0.3:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(80, 200)
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Keep particles on screen
            x = max(50, min(750, x))
            y = max(50, min(550, y))
            
            particles.append(Particle(x, y))
        
        # Update and draw particles
        for particle in particles[:]:
            particle.update(center_x, center_y, current_time, params)
            if particle.life <= 0:
                particles.remove(particle)
            else:
                particle.draw(canvas)
        
        # Draw enhanced center point
        pulse = 8 + 5 * math.sin(current_time * 0.005)
        glow_pulse = 15 + 8 * math.sin(current_time * 0.003)
        
        # Outer glow
        canvas.create_oval(center_x-glow_pulse, center_y-glow_pulse, 
                          center_x+glow_pulse, center_y+glow_pulse, 
                          fill="", outline="cyan", width=1)
        
        # Inner core
        canvas.create_oval(center_x-pulse, center_y-pulse, 
                          center_x+pulse, center_y+pulse, 
                          fill="white", outline="yellow", width=2)
        
        # Add parameter display
        canvas.create_text(400, 20, text="Interactive Particle Flow Explorer", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(400, 40, text=f"Particles: {len(particles)} | Flow: {params['strength']:.2f} | Complexity: {params['complexity']:.3f}", 
                          fill="cyan", font=("Arial", 10))
        
        # Schedule next frame
        root.after(30, draw_frame)
    
    # Bind escape key to close
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    create_interactive_particle_flow()
