import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame, Button
import math
import time

class CelestialBody:
    """A celestial body with mass, position, velocity, and gravitational effects"""
    def __init__(self, x, y, vx, vy, mass, radius, color, name="Body"):
        self.x = x
        self.y = y
        self.vx = vx  # velocity in x direction
        self.vy = vy  # velocity in y direction
        self.mass = mass
        self.radius = radius  # visual size (not to scale)
        self.color = color
        self.name = name
        self.trail = []  # stores previous positions for drawing trails
        self.ax = 0  # acceleration in x direction
        self.ay = 0  # acceleration in y direction
    
    def update_position(self, dt):
        """Update position based on current velocity"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        
        # Limit trail length for performance and visibility
        if self.name == "Sun":
            trail_length = 200  # Sun shows barycentric wobble
        elif self.name == "Earth":
            trail_length = 800  # Show multiple Earth orbits
        else:  # Moon
            trail_length = 1000  # Show Moon's complete epicycloid pattern
            
        if len(self.trail) > trail_length:
            self.trail.pop(0)
    
    def update_velocity(self, dt):
        """Update velocity based on current acceleration"""
        self.vx += self.ax * dt
        self.vy += self.ay * dt
    
    def reset_acceleration(self):
        """Reset acceleration to zero (called each frame)"""
        self.ax = 0
        self.ay = 0
    
    def add_gravitational_force(self, other_body, G):
        """Calculate and add gravitational force from another body"""
        # Calculate distance between bodies
        dx = other_body.x - self.x
        dy = other_body.y - self.y
        distance_squared = dx*dx + dy*dy
        distance = math.sqrt(distance_squared)
        
        # Avoid division by zero and excessive forces at very small distances
        min_distance = (self.radius + other_body.radius) * 0.5
        if distance < min_distance:
            distance = min_distance
            distance_squared = distance * distance
        
        # Newton's Law: F = G * m1 * m2 / r^2
        force_magnitude = G * self.mass * other_body.mass / distance_squared
        
        # Calculate force direction (unit vector)
        force_x = force_magnitude * dx / distance
        force_y = force_magnitude * dy / distance
        
        # F = ma, so a = F/m (acceleration = force / mass)
        self.ax += force_x / self.mass
        self.ay += force_y / self.mass
    
    def draw(self, canvas, center_x, center_y, scale):
        """Draw the celestial body and its trail"""
        # Convert world coordinates to screen coordinates
        screen_x = center_x + self.x * scale
        screen_y = center_y + self.y * scale
        
        # Draw trail with fading effect
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                # Calculate fade based on position in trail
                fade = i / len(self.trail)
                
                # Create fading color (simpler approach)
                if fade < 0.3:
                    trail_color = "#333333"  # Very dark
                elif fade < 0.6:
                    if self.color == '#ffff00':  # Sun
                        trail_color = "#666600"
                    elif self.color == '#4169e1':  # Earth
                        trail_color = "#003366"
                    else:  # Moon
                        trail_color = "#666666"
                else:
                    if self.color == '#ffff00':  # Sun
                        trail_color = "#cccc00"
                    elif self.color == '#4169e1':  # Earth
                        trail_color = "#0066cc"
                    else:  # Moon
                        trail_color = "#999999"
                
                x1 = center_x + self.trail[i-1][0] * scale
                y1 = center_y + self.trail[i-1][1] * scale
                x2 = center_x + self.trail[i][0] * scale
                y2 = center_y + self.trail[i][1] * scale
                
                # Only draw if on screen
                if (-50 < x1 < 1000 and -50 < y1 < 800 and 
                    -50 < x2 < 1000 and -50 < y2 < 800):
                    canvas.create_line(x1, y1, x2, y2, fill=trail_color, width=2)
        
        # Draw the body itself (only if on screen)
        if -50 < screen_x < 1000 and -50 < screen_y < 800:
            canvas.create_oval(
                screen_x - self.radius, screen_y - self.radius,
                screen_x + self.radius, screen_y + self.radius,
                fill=self.color, outline="white", width=2
            )
            
            # Draw name label
            canvas.create_text(screen_x, screen_y - self.radius - 15, 
                              text=self.name, fill="white", font=("Arial", 10, "bold"))

def create_earth_moon_sun_simulation():
    """Create an interactive Earth-Moon-Sun three-body simulation"""
    root = tk.Tk()
    root.title("Earth-Moon-Sun Three-Body Simulation")
    root.geometry("1400x900")
    root.configure(bg='black')
    
    # Create main frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Canvas for simulation
    canvas = Canvas(main_frame, width=1000, height=700, bg='#000011')
    canvas.pack(side=tk.LEFT, padx=(0, 20))
    
    # Control panel
    control_frame = Frame(main_frame, bg='black', width=350)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)
    control_frame.pack_propagate(False)
    
    # Physical constants (scaled for visualization)
    G_real = 6.67430e-11  # Real gravitational constant
    M_sun_real = 1.989e30  # Real Sun mass
    M_earth_real = 5.972e24  # Real Earth mass
    M_moon_real = 7.342e22  # Real Moon mass
    
    # Distances (scaled for visualization)
    earth_sun_distance_real = 1.496e11  # 1 AU
    earth_moon_distance_real = 3.844e8  # Earth-Moon distance
    
    # Scale factors for simulation (adjusted for screen visibility)
    # We need Earth to be about 150-200 pixels from center to be visible
    earth_sun_distance = 180  # pixels from center to Earth
    earth_moon_distance = 15   # pixels from Earth to Moon (much closer!)
    
    # Calculate masses to maintain realistic orbital periods
    # Using simplified units where G=1 for easier calculation
    M_sun = 800   # Large mass for Sun to dominate the system
    M_earth = 12  # Larger Earth mass for stronger Moon binding
    M_moon = 0.3  # Smaller Moon mass to reduce perturbations
    
    # Simulation parameters
    G = tk.DoubleVar(value=1.0)  # Gravitational constant (simplified units)
    time_step = tk.DoubleVar(value=0.03)  # Balanced time step for natural dynamics
    zoom = tk.DoubleVar(value=1.5)  # Zoom factor (reduced for wider view)
    trail_speed = tk.IntVar(value=1)  # Animation speed
    
    # Create celestial bodies
    bodies = []
    
    def reset_simulation():
        """Reset the simulation to initial conditions"""
        nonlocal bodies
        bodies.clear()
        
        # Sun at center
        sun = CelestialBody(0, 0, 0, 0, M_sun, 25, '#ffff00', "Sun")
        
        # Calculate the Earth-Moon system's orbital velocity around the Sun
        system_orbital_velocity = math.sqrt(G.get() * M_sun / earth_sun_distance)
        
        # Earth starts at distance from Sun
        earth = CelestialBody(earth_sun_distance, 0, 0, system_orbital_velocity, 
                             M_earth, 18, '#4169e1', "Earth")
        
        # Moon starts perpendicular to Earth-Sun line for stable orbit
        moon_x = earth_sun_distance
        moon_y = earth_moon_distance  # Position Moon "above" Earth
        
        # Calculate Moon's orbital velocity for ~27 day period around Earth
        # For realistic periods: Earth should take ~365 simulation days, Moon ~27 days around Earth
        
        # Moon's orbital velocity around Earth (for 27-day period)
        # We need to scale this so Moon completes ~13.5 orbits while Earth completes 1 solar orbit
        # Current observation: Moon barely moves in 56 days, need MUCH more speed
        moon_orbital_velocity_relative = math.sqrt(G.get() * M_earth / earth_moon_distance) * 25.0  # Dramatically faster!
        
        # Moon's total velocity = Earth's velocity + orbital component around Earth
        moon_vx = system_orbital_velocity  # Same as Earth around Sun
        moon_vy = moon_orbital_velocity_relative  # Velocity to orbit Earth in ~27 days
        
        moon = CelestialBody(moon_x, moon_y, moon_vx, moon_vy, M_moon, 8, '#c0c0c0', "Moon")
        
        bodies = [sun, earth, moon]
    
    def create_slider(parent, label, variable, from_, to, resolution=0.1):
        frame = Frame(parent, bg='black')
        frame.pack(fill=tk.X, pady=5)
        
        Label(frame, text=label, fg="white", bg="black", 
              font=("Arial", 11, "bold")).pack()
        slider = Scale(frame, from_=from_, to=to, resolution=resolution, 
                      orient=tk.HORIZONTAL, variable=variable, 
                      bg="gray20", fg="white", highlightbackground="black",
                      length=300)
        slider.pack(fill=tk.X)
        return slider
    
    # Create control sliders
    Label(control_frame, text="Earth-Moon-Sun Simulation", 
          font=("Arial", 16, "bold"), fg="yellow", bg="black").pack(pady=10)
    
    create_slider(control_frame, "Gravitational Strength", G, 0.1, 5.0, 0.1)
    create_slider(control_frame, "Time Step", time_step, 0.01, 0.5, 0.01)
    create_slider(control_frame, "Zoom Level", zoom, 0.2, 5.0, 0.1)
    create_slider(control_frame, "Animation Speed", trail_speed, 1, 5, 1)
    
    # Information display
    info_frame = Frame(control_frame, bg='black')
    info_frame.pack(pady=20)
    
    day_label = Label(info_frame, text="Day: 0", fg="cyan", bg="black", 
                     font=("Arial", 12, "bold"))
    day_label.pack()
    
    distance_label = Label(info_frame, text="", fg="lightgreen", bg="black", 
                          font=("Arial", 10))
    distance_label.pack()
    
    # Control buttons
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    Button(button_frame, text="Reset Simulation", command=reset_simulation,
           bg="orange", fg="black", font=("Arial", 12, "bold"), width=20).pack(pady=5)
    
    def toggle_pause():
        nonlocal paused
        paused = not paused
        pause_button.config(text="Resume" if paused else "Pause")
    
    pause_button = Button(button_frame, text="Pause", command=toggle_pause,
                         bg="red", fg="white", font=("Arial", 12, "bold"), width=20)
    pause_button.pack(pady=5)
    
    # Instructions
    Label(control_frame, text="Three-Body Physics:", 
          font=("Arial", 14, "bold"), fg="yellow", bg="black").pack(pady=(20,5))
    
    physics_info = """• Sun: Massive central star
• Earth: Orbits Sun in ~365 days
• Moon: Orbits Earth in ~27 days
• Moon should complete ~13.5 orbits 
  around Earth per Earth solar orbit
• All bodies attract each other!
• Adjust gravity to see effects
• Watch the complex dance!"""
    
    Label(control_frame, text=physics_info, 
          font=("Arial", 10), fg="white", bg="black", justify=tk.LEFT).pack(pady=5)
    
    # Simulation variables
    day_counter = 0
    paused = False
    
    def simulate_physics():
        """Main physics simulation step"""
        if len(bodies) < 2 or paused:
            return
        
        dt = time_step.get()  # Use time step directly
        gravity_constant = G.get()  # Use G directly
        
        # Reset all accelerations
        for body in bodies:
            body.reset_acceleration()
        
        # Calculate gravitational forces between all pairs of bodies
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                body1 = bodies[i]
                body2 = bodies[j]
                
                # Apply Newton's law of gravitation
                body1.add_gravitational_force(body2, gravity_constant)
                body2.add_gravitational_force(body1, gravity_constant)
        
        # Update velocities and positions
        for body in bodies:
            body.update_velocity(dt)
            body.update_position(dt)
        
        # Apply soft constraint to keep Moon in reasonable orbit around Earth
        if len(bodies) >= 3:
            earth = bodies[1]
            moon = bodies[2]
            
            # Calculate Earth-Moon distance
            dx = moon.x - earth.x
            dy = moon.y - earth.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # If Moon is getting too far or too close, apply gentle correction
            ideal_distance = earth_moon_distance
            if distance > ideal_distance * 4.0:  # Much more tolerance for very fast orbit
                correction_strength = 0.01  # Very gentle correction
                moon.vx -= correction_strength * dx / distance
                moon.vy -= correction_strength * dy / distance
            elif distance < ideal_distance * 0.1:  # Too close
                correction_strength = 0.005  # Extremely gentle correction
                moon.vx += correction_strength * dx / distance
                moon.vy += correction_strength * dy / distance
    
    def draw_frame():
        """Draw the current frame of the simulation"""
        nonlocal day_counter
        
        canvas.delete("all")
        
        # Get canvas center and zoom
        center_x, center_y = 500, 350
        scale = zoom.get()
        
        # Draw grid for reference
        grid_spacing = int(50 / scale)
        if grid_spacing > 10:
            for i in range(-500, 501, grid_spacing):
                canvas.create_line(center_x + i * scale, 0, 
                                 center_x + i * scale, 700, 
                                 fill="#333333", width=1)
            for i in range(-350, 351, grid_spacing):
                canvas.create_line(0, center_y + i * scale, 
                                 1000, center_y + i * scale, 
                                 fill="#333333", width=1)
        
        # Draw all celestial bodies
        for body in bodies:
            body.draw(canvas, center_x, center_y, scale)
        
        # Display information
        canvas.create_text(500, 30, text="Earth-Moon-Sun Three-Body Simulation", 
                          fill="yellow", font=("Arial", 18, "bold"))
        
        info_text = f"Day: {day_counter:.1f} | Bodies: {len(bodies)} | Zoom: {zoom.get():.1f}x"
        canvas.create_text(500, 60, text=info_text, 
                          fill="cyan", font=("Arial", 12))
        
        # Calculate and display distances
        if len(bodies) >= 3:
            sun, earth, moon = bodies[0], bodies[1], bodies[2]
            
            sun_earth_dist = math.sqrt((earth.x - sun.x)**2 + (earth.y - sun.y)**2)
            earth_moon_dist = math.sqrt((moon.x - earth.x)**2 + (moon.y - earth.y)**2)
            
            day_label.config(text=f"Day: {day_counter:.1f}")
            distance_label.config(text=f"Sun-Earth: {sun_earth_dist:.1f}\nEarth-Moon: {earth_moon_dist:.1f}")
        
        # Update physics and increment day counter
        for _ in range(trail_speed.get()):
            simulate_physics()
            day_counter += time_step.get() * 5  # Adjusted scale for realistic day progression
        
        # Schedule next frame
        root.after(50, draw_frame)
    
    # Initialize simulation
    reset_simulation()
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    print("Starting Earth-Moon-Sun Three-Body Simulation...")
    print("This shows how Earth and Moon orbit the Sun together!")
    print("Use the controls to adjust physics parameters.")
    create_earth_moon_sun_simulation()
