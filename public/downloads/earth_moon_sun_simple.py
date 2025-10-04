import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame, Button
import math

def create_earth_moon_sun_simulation():
    """Create a simple, accurate Earth-Moon-Sun simulation using trigonometric orbits"""
    
    # Create main window
    root = tk.Tk()
    root.title("Earth-Moon-Sun Simple Simulation")
    root.geometry("1200x800")
    root.configure(bg='black')
    
    # Create main frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create canvas for simulation
    canvas = Canvas(main_frame, width=800, height=700, bg='black')
    canvas.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Create control panel
    control_frame = Frame(main_frame, bg='black', width=300)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
    control_frame.pack_propagate(False)
    
    # Constants (scaled for visualization)
    AU = 200  # Earth-Sun distance in pixels
    earth_orbital_period = 365.25  # days
    moon_orbital_period = 27.3     # days
    moon_orbit_radius = AU * 0.08  # Moon-Earth distance in pixels (~16 pixels)
    
    # Simulation parameters
    time_speed = tk.DoubleVar(value=2.0)  # days per frame
    zoom = tk.DoubleVar(value=1.0)
    trail_length = tk.IntVar(value=500)
    
    # Storage for trails
    earth_trail = []
    moon_trail = []
    
    # Current time
    current_day = [0.0]  # Use list to make it mutable
    paused = [False]
    
    # Visibility toggles
    show_earth = [True]
    show_moon = [True]
    show_earth_trail = [True]
    show_moon_trail = [True]
    
    def create_slider(parent, label, variable, from_, to, resolution=0.1):
        frame = Frame(parent, bg='black')
        frame.pack(fill=tk.X, pady=5)
        
        Label(frame, text=label, fg="white", bg="black", 
              font=("Arial", 11, "bold")).pack()
        slider = Scale(frame, from_=from_, to=to, resolution=resolution, 
                      orient=tk.HORIZONTAL, variable=variable, 
                      bg="gray20", fg="white", highlightbackground="black",
                      length=250)
        slider.pack(fill=tk.X)
        return slider
    
    # Create controls
    Label(control_frame, text="Earth-Moon-Sun Simulation", 
          font=("Arial", 16, "bold"), fg="yellow", bg="black").pack(pady=10)
    
    create_slider(control_frame, "Time Speed (days/frame)", time_speed, 0.1, 10.0, 0.1)
    create_slider(control_frame, "Zoom Level", zoom, 0.3, 3.0, 0.1)
    create_slider(control_frame, "Trail Length", trail_length, 50, 1000, 50)
    
    # Information display
    info_frame = Frame(control_frame, bg='black')
    info_frame.pack(pady=20)
    
    day_label = Label(info_frame, text="Day: 0.0", fg="cyan", bg="black", 
                     font=("Arial", 12, "bold"))
    day_label.pack()
    
    year_label = Label(info_frame, text="Year: 0.0", fg="cyan", bg="black", 
                      font=("Arial", 12, "bold"))
    year_label.pack()
    
    moon_phase_label = Label(info_frame, text="Moon Orbits: 0.0", fg="cyan", bg="black", 
                            font=("Arial", 12, "bold"))
    moon_phase_label.pack()
    
    # Control buttons
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    def reset_simulation():
        current_day[0] = 0.0
        earth_trail.clear()
        moon_trail.clear()
    
    def toggle_pause():
        paused[0] = not paused[0]
        pause_button.config(text="Resume" if paused[0] else "Pause")
    
    reset_button = Button(button_frame, text="Reset Simulation", command=reset_simulation,
                         bg="orange", fg="black", font=("Arial", 12, "bold"), width=20)
    reset_button.pack(pady=5)
    
    pause_button = Button(button_frame, text="Pause", command=toggle_pause,
                         bg="red", fg="white", font=("Arial", 12, "bold"), width=20)
    pause_button.pack(pady=5)
    
    # Visibility toggle functions
    def toggle_earth():
        show_earth[0] = not show_earth[0]
        earth_button.config(text=f"Earth: {'ON' if show_earth[0] else 'OFF'}",
                           bg="#4169e1" if show_earth[0] else "gray")
    
    def toggle_moon():
        show_moon[0] = not show_moon[0]
        moon_button.config(text=f"Moon: {'ON' if show_moon[0] else 'OFF'}",
                          bg="#c0c0c0" if show_moon[0] else "gray")
    
    def toggle_earth_trail():
        show_earth_trail[0] = not show_earth_trail[0]
        earth_trail_button.config(text=f"Earth Trail: {'ON' if show_earth_trail[0] else 'OFF'}",
                                 bg="#1e90ff" if show_earth_trail[0] else "gray")
    
    def toggle_moon_trail():
        show_moon_trail[0] = not show_moon_trail[0]
        moon_trail_button.config(text=f"Moon Trail: {'ON' if show_moon_trail[0] else 'OFF'}",
                                bg="#ffffff" if show_moon_trail[0] else "gray")
    
    # Visibility toggle buttons
    visibility_frame = Frame(control_frame, bg='black')
    visibility_frame.pack(pady=10)
    
    Label(visibility_frame, text="Show/Hide Objects:", 
          font=("Arial", 12, "bold"), fg="yellow", bg="black").pack(pady=(0,5))
    
    earth_button = Button(visibility_frame, text="Earth: ON", command=toggle_earth,
                         bg="#4169e1", fg="white", font=("Arial", 10, "bold"), width=18)
    earth_button.pack(pady=2)
    
    moon_button = Button(visibility_frame, text="Moon: ON", command=toggle_moon,
                        bg="#c0c0c0", fg="black", font=("Arial", 10, "bold"), width=18)
    moon_button.pack(pady=2)
    
    earth_trail_button = Button(visibility_frame, text="Earth Trail: ON", command=toggle_earth_trail,
                               bg="#1e90ff", fg="white", font=("Arial", 10, "bold"), width=18)
    earth_trail_button.pack(pady=2)
    
    moon_trail_button = Button(visibility_frame, text="Moon Trail: ON", command=toggle_moon_trail,
                              bg="#ffffff", fg="black", font=("Arial", 10, "bold"), width=18)
    moon_trail_button.pack(pady=2)
    
    # Instructions
    Label(control_frame, text="Orbital Mechanics:", 
          font=("Arial", 14, "bold"), fg="yellow", bg="black").pack(pady=(20,5))
    
    physics_info = """• Earth orbits Sun in 365.25 days
• Moon orbits Earth in 27.3 days
• Moon completes ~13.4 orbits per Earth year
• Simple trigonometric calculations
• Mathematically accurate periods
• Beautiful epicycloid patterns"""
    
    Label(control_frame, text=physics_info, 
          font=("Arial", 10), fg="white", bg="black", justify=tk.LEFT).pack(pady=5)
    
    def calculate_positions(day):
        """Calculate Earth and Moon positions using simple trigonometry"""
        # Earth position around Sun (circular orbit)
        earth_angle = 2 * math.pi * day / earth_orbital_period
        earth_x = AU * math.cos(earth_angle)
        earth_y = AU * math.sin(earth_angle)
        
        # Moon position relative to Earth (circular orbit)
        moon_angle = 2 * math.pi * day / moon_orbital_period
        moon_x_rel = moon_orbit_radius * math.cos(moon_angle)
        moon_y_rel = moon_orbit_radius * math.sin(moon_angle)
        
        # Moon absolute position (Earth + relative)
        moon_x = earth_x + moon_x_rel
        moon_y = earth_y + moon_y_rel
        
        return earth_x, earth_y, moon_x, moon_y
    
    def draw_frame():
        """Draw the current frame of the simulation"""
        if not paused[0]:
            current_day[0] += time_speed.get()
        
        canvas.delete("all")
        
        # Get canvas center and zoom
        center_x, center_y = 400, 350
        scale = zoom.get()
        
        # Calculate current positions
        earth_x, earth_y, moon_x, moon_y = calculate_positions(current_day[0])
        
        # Add to trails
        earth_trail.append((earth_x, earth_y))
        moon_trail.append((moon_x, moon_y))
        
        # Limit trail lengths
        max_trail = trail_length.get()
        if len(earth_trail) > max_trail:
            earth_trail.pop(0)
        if len(moon_trail) > max_trail:
            moon_trail.pop(0)
        
        # Draw trails (only if enabled)
        if show_earth_trail[0] and len(earth_trail) > 1:
            for i in range(1, len(earth_trail)):
                fade = i / len(earth_trail)
                if fade > 0.3:  # Only draw recent trail
                    x1 = center_x + earth_trail[i-1][0] * scale
                    y1 = center_y + earth_trail[i-1][1] * scale
                    x2 = center_x + earth_trail[i][0] * scale
                    y2 = center_y + earth_trail[i][1] * scale
                    
                    color = f"#{int(65*fade):02x}{int(105*fade):02x}{int(225*fade):02x}"
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        if show_moon_trail[0] and len(moon_trail) > 1:
            for i in range(1, len(moon_trail)):
                fade = i / len(moon_trail)
                if fade > 0.2:  # Only draw recent trail
                    x1 = center_x + moon_trail[i-1][0] * scale
                    y1 = center_y + moon_trail[i-1][1] * scale
                    x2 = center_x + moon_trail[i][0] * scale
                    y2 = center_y + moon_trail[i][1] * scale
                    
                    color = f"#{int(192*fade):02x}{int(192*fade):02x}{int(192*fade):02x}"
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
        
        # Draw Sun at center
        sun_x = center_x
        sun_y = center_y
        canvas.create_oval(sun_x-15, sun_y-15, sun_x+15, sun_y+15, 
                          fill='#ffff00', outline='#ffaa00', width=2)
        canvas.create_text(sun_x, sun_y-25, text="Sun", fill="yellow", 
                          font=("Arial", 10, "bold"))
        
        # Draw Earth (only if enabled)
        if show_earth[0]:
            screen_earth_x = center_x + earth_x * scale
            screen_earth_y = center_y + earth_y * scale
            canvas.create_oval(screen_earth_x-8, screen_earth_y-8, 
                              screen_earth_x+8, screen_earth_y+8, 
                              fill='#4169e1', outline='#1e90ff', width=2)
            canvas.create_text(screen_earth_x, screen_earth_y-18, text="Earth", 
                              fill="lightblue", font=("Arial", 9, "bold"))
        
        # Draw Moon (only if enabled)
        if show_moon[0]:
            screen_moon_x = center_x + moon_x * scale
            screen_moon_y = center_y + moon_y * scale
            canvas.create_oval(screen_moon_x-4, screen_moon_y-4, 
                              screen_moon_x+4, screen_moon_y+4, 
                              fill='#c0c0c0', outline='#ffffff', width=1)
            canvas.create_text(screen_moon_x, screen_moon_y-12, text="Moon", 
                              fill="white", font=("Arial", 8, "bold"))
        
        # Update information
        years = current_day[0] / 365.25
        moon_orbits = current_day[0] / moon_orbital_period
        
        day_label.config(text=f"Day: {current_day[0]:.1f}")
        year_label.config(text=f"Year: {years:.3f}")
        moon_phase_label.config(text=f"Moon Orbits: {moon_orbits:.1f}")
        
        # Schedule next frame
        root.after(50, draw_frame)
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    print("Starting Simple Earth-Moon-Sun Simulation...")
    print("This uses clean trigonometric calculations for accurate orbital periods!")
    create_earth_moon_sun_simulation()
