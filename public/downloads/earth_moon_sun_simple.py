import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame, Button
import math

def create_earth_moon_sun_simulation():
    """Create a simple, accurate Earth-Moon-Sun simulation using trigonometric orbits"""
    
    # Create main window
    root = tk.Tk()
    root.title("Solar System Orbital Mechanics - Earth, Moon, Mars & Moons")
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
    
    # Mars system constants
    mars_orbital_period = 687.0    # days (Mars year)
    mars_distance = AU * 1.52      # Mars-Sun distance (1.52 AU)
    phobos_orbital_period = 0.32   # days (7.6 hours)
    deimos_orbital_period = 1.26   # days (30.3 hours)
    phobos_orbit_radius = AU * 0.02  # Phobos-Mars distance (~4 pixels)
    deimos_orbit_radius = AU * 0.035 # Deimos-Mars distance (~7 pixels)
    
    # Simulation parameters
    time_speed = tk.DoubleVar(value=2.0)  # days per frame
    zoom = tk.DoubleVar(value=1.0)
    trail_length = tk.IntVar(value=500)
    
    # Storage for trails
    earth_trail = []
    moon_trail = []
    mars_trail = []
    phobos_trail = []
    deimos_trail = []
    
    # Current time
    current_day = [0.0]  # Use list to make it mutable
    paused = [False]
    
    # Visibility toggles
    show_earth = [True]
    show_moon = [True]
    show_earth_trail = [True]
    show_moon_trail = [True]
    show_mars = [True]
    show_phobos = [True]
    show_deimos = [True]
    show_mars_trail = [True]
    show_phobos_trail = [True]
    show_deimos_trail = [True]
    
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
    Label(control_frame, text="Solar System Simulation", 
          font=("Arial", 16, "bold"), fg="yellow", bg="black").pack(pady=10)
    
    create_slider(control_frame, "Time Speed (days/frame)", time_speed, 0.01, 10.0, 0.01)
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
    
    mars_year_label = Label(info_frame, text="Mars Year: 0.0", fg="orange", bg="black", 
                           font=("Arial", 12, "bold"))
    mars_year_label.pack()
    
    phobos_orbits_label = Label(info_frame, text="Phobos Orbits: 0.0", fg="goldenrod", bg="black", 
                               font=("Arial", 12, "bold"))
    phobos_orbits_label.pack()
    
    # Control buttons
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    def reset_simulation():
        current_day[0] = 0.0
        earth_trail.clear()
        moon_trail.clear()
        mars_trail.clear()
        phobos_trail.clear()
        deimos_trail.clear()
    
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
    
    def toggle_mars():
        show_mars[0] = not show_mars[0]
        mars_button.config(text=f"Mars: {'ON' if show_mars[0] else 'OFF'}",
                          bg="#cd5c5c" if show_mars[0] else "gray")
    
    def toggle_phobos():
        show_phobos[0] = not show_phobos[0]
        phobos_button.config(text=f"Phobos: {'ON' if show_phobos[0] else 'OFF'}",
                            bg="#8b7355" if show_phobos[0] else "gray")
    
    def toggle_deimos():
        show_deimos[0] = not show_deimos[0]
        deimos_button.config(text=f"Deimos: {'ON' if show_deimos[0] else 'OFF'}",
                            bg="#696969" if show_deimos[0] else "gray")
    
    def toggle_mars_trail():
        show_mars_trail[0] = not show_mars_trail[0]
        mars_trail_button.config(text=f"Mars Trail: {'ON' if show_mars_trail[0] else 'OFF'}",
                                bg="#ff6347" if show_mars_trail[0] else "gray")
    
    def toggle_phobos_trail():
        show_phobos_trail[0] = not show_phobos_trail[0]
        phobos_trail_button.config(text=f"Phobos Trail: {'ON' if show_phobos_trail[0] else 'OFF'}",
                                  bg="#daa520" if show_phobos_trail[0] else "gray")
    
    def toggle_deimos_trail():
        show_deimos_trail[0] = not show_deimos_trail[0]
        deimos_trail_button.config(text=f"Deimos Trail: {'ON' if show_deimos_trail[0] else 'OFF'}",
                                  bg="#a9a9a9" if show_deimos_trail[0] else "gray")
    
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
    
    # Mars system buttons
    Label(visibility_frame, text="Mars System:", 
          font=("Arial", 11, "bold"), fg="orange", bg="black").pack(pady=(10,5))
    
    mars_button = Button(visibility_frame, text="Mars: ON", command=toggle_mars,
                        bg="#cd5c5c", fg="white", font=("Arial", 10, "bold"), width=18)
    mars_button.pack(pady=2)
    
    phobos_button = Button(visibility_frame, text="Phobos: ON", command=toggle_phobos,
                          bg="#8b7355", fg="white", font=("Arial", 10, "bold"), width=18)
    phobos_button.pack(pady=2)
    
    deimos_button = Button(visibility_frame, text="Deimos: ON", command=toggle_deimos,
                          bg="#696969", fg="white", font=("Arial", 10, "bold"), width=18)
    deimos_button.pack(pady=2)
    
    mars_trail_button = Button(visibility_frame, text="Mars Trail: ON", command=toggle_mars_trail,
                              bg="#ff6347", fg="white", font=("Arial", 10, "bold"), width=18)
    mars_trail_button.pack(pady=2)
    
    phobos_trail_button = Button(visibility_frame, text="Phobos Trail: ON", command=toggle_phobos_trail,
                                bg="#daa520", fg="black", font=("Arial", 10, "bold"), width=18)
    phobos_trail_button.pack(pady=2)
    
    deimos_trail_button = Button(visibility_frame, text="Deimos Trail: ON", command=toggle_deimos_trail,
                                bg="#a9a9a9", fg="white", font=("Arial", 10, "bold"), width=18)
    deimos_trail_button.pack(pady=2)
    
    # Instructions
    Label(control_frame, text="Orbital Mechanics:", 
          font=("Arial", 14, "bold"), fg="yellow", bg="black").pack(pady=(20,5))
    
    physics_info = """• Earth orbits Sun in 365.25 days
• Moon orbits Earth in 27.3 days
• Mars orbits Sun in 687 days (1.88 Earth years)
• Phobos orbits Mars in 0.32 days (7.6 hours)
• Deimos orbits Mars in 1.26 days (30.3 hours)
• Simple trigonometric calculations
• Mathematically accurate periods
• Beautiful epicycloid patterns"""
    
    Label(control_frame, text=physics_info, 
          font=("Arial", 10), fg="white", bg="black", justify=tk.LEFT).pack(pady=5)
    
    def calculate_positions(day):
        """Calculate positions of all celestial bodies using simple trigonometry"""
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
        
        # Mars position around Sun (circular orbit)
        mars_angle = 2 * math.pi * day / mars_orbital_period
        mars_x = mars_distance * math.cos(mars_angle)
        mars_y = mars_distance * math.sin(mars_angle)
        
        # Phobos position relative to Mars (circular orbit)
        phobos_angle = 2 * math.pi * day / phobos_orbital_period
        phobos_x_rel = phobos_orbit_radius * math.cos(phobos_angle)
        phobos_y_rel = phobos_orbit_radius * math.sin(phobos_angle)
        
        # Phobos absolute position (Mars + relative)
        phobos_x = mars_x + phobos_x_rel
        phobos_y = mars_y + phobos_y_rel
        
        # Deimos position relative to Mars (circular orbit)
        deimos_angle = 2 * math.pi * day / deimos_orbital_period
        deimos_x_rel = deimos_orbit_radius * math.cos(deimos_angle)
        deimos_y_rel = deimos_orbit_radius * math.sin(deimos_angle)
        
        # Deimos absolute position (Mars + relative)
        deimos_x = mars_x + deimos_x_rel
        deimos_y = mars_y + deimos_y_rel
        
        return earth_x, earth_y, moon_x, moon_y, mars_x, mars_y, phobos_x, phobos_y, deimos_x, deimos_y
    
    def draw_frame():
        """Draw the current frame of the simulation"""
        if not paused[0]:
            current_day[0] += time_speed.get()
        
        canvas.delete("all")
        
        # Get canvas center and zoom
        center_x, center_y = 400, 350
        scale = zoom.get()
        
        # Calculate current positions
        earth_x, earth_y, moon_x, moon_y, mars_x, mars_y, phobos_x, phobos_y, deimos_x, deimos_y = calculate_positions(current_day[0])
        
        # Add to trails
        earth_trail.append((earth_x, earth_y))
        moon_trail.append((moon_x, moon_y))
        mars_trail.append((mars_x, mars_y))
        phobos_trail.append((phobos_x, phobos_y))
        deimos_trail.append((deimos_x, deimos_y))
        
        # Limit trail lengths
        max_trail = trail_length.get()
        if len(earth_trail) > max_trail:
            earth_trail.pop(0)
        if len(moon_trail) > max_trail:
            moon_trail.pop(0)
        if len(mars_trail) > max_trail:
            mars_trail.pop(0)
        if len(phobos_trail) > max_trail:
            phobos_trail.pop(0)
        if len(deimos_trail) > max_trail:
            deimos_trail.pop(0)
        
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
        
        # Draw Mars system trails
        if show_mars_trail[0] and len(mars_trail) > 1:
            for i in range(1, len(mars_trail)):
                fade = i / len(mars_trail)
                if fade > 0.3:  # Only draw recent trail
                    x1 = center_x + mars_trail[i-1][0] * scale
                    y1 = center_y + mars_trail[i-1][1] * scale
                    x2 = center_x + mars_trail[i][0] * scale
                    y2 = center_y + mars_trail[i][1] * scale
                    
                    color = f"#{int(205*fade):02x}{int(92*fade):02x}{int(92*fade):02x}"
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        if show_phobos_trail[0] and len(phobos_trail) > 1:
            for i in range(1, len(phobos_trail)):
                fade = i / len(phobos_trail)
                if fade > 0.2:  # Only draw recent trail
                    x1 = center_x + phobos_trail[i-1][0] * scale
                    y1 = center_y + phobos_trail[i-1][1] * scale
                    x2 = center_x + phobos_trail[i][0] * scale
                    y2 = center_y + phobos_trail[i][1] * scale
                    
                    color = f"#{int(218*fade):02x}{int(165*fade):02x}{int(32*fade):02x}"
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
        
        if show_deimos_trail[0] and len(deimos_trail) > 1:
            for i in range(1, len(deimos_trail)):
                fade = i / len(deimos_trail)
                if fade > 0.2:  # Only draw recent trail
                    x1 = center_x + deimos_trail[i-1][0] * scale
                    y1 = center_y + deimos_trail[i-1][1] * scale
                    x2 = center_x + deimos_trail[i][0] * scale
                    y2 = center_y + deimos_trail[i][1] * scale
                    
                    color = f"#{int(169*fade):02x}{int(169*fade):02x}{int(169*fade):02x}"
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
        
        # Draw Mars system (only if enabled)
        if show_mars[0]:
            screen_mars_x = center_x + mars_x * scale
            screen_mars_y = center_y + mars_y * scale
            canvas.create_oval(screen_mars_x-6, screen_mars_y-6, 
                              screen_mars_x+6, screen_mars_y+6, 
                              fill='#cd5c5c', outline='#ff6347', width=2)
            canvas.create_text(screen_mars_x, screen_mars_y-16, text="Mars", 
                              fill="orange", font=("Arial", 9, "bold"))
        
        if show_phobos[0]:
            screen_phobos_x = center_x + phobos_x * scale
            screen_phobos_y = center_y + phobos_y * scale
            canvas.create_oval(screen_phobos_x-2, screen_phobos_y-2, 
                              screen_phobos_x+2, screen_phobos_y+2, 
                              fill='#8b7355', outline='#daa520', width=1)
            canvas.create_text(screen_phobos_x, screen_phobos_y-10, text="Phobos", 
                              fill="goldenrod", font=("Arial", 7, "bold"))
        
        if show_deimos[0]:
            screen_deimos_x = center_x + deimos_x * scale
            screen_deimos_y = center_y + deimos_y * scale
            canvas.create_oval(screen_deimos_x-2, screen_deimos_y-2, 
                              screen_deimos_x+2, screen_deimos_y+2, 
                              fill='#696969', outline='#a9a9a9', width=1)
            canvas.create_text(screen_deimos_x, screen_deimos_y-10, text="Deimos", 
                              fill="lightgray", font=("Arial", 7, "bold"))
        
        # Update information
        years = current_day[0] / 365.25
        moon_orbits = current_day[0] / moon_orbital_period
        mars_years = current_day[0] / mars_orbital_period
        phobos_orbits = current_day[0] / phobos_orbital_period
        
        day_label.config(text=f"Day: {current_day[0]:.1f}")
        year_label.config(text=f"Year: {years:.3f}")
        moon_phase_label.config(text=f"Moon Orbits: {moon_orbits:.1f}")
        mars_year_label.config(text=f"Mars Year: {mars_years:.3f}")
        phobos_orbits_label.config(text=f"Phobos Orbits: {phobos_orbits:.0f}")
        
        # Schedule next frame
        root.after(50, draw_frame)
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    print("Starting Solar System Orbital Mechanics Simulation...")
    print("Features Earth, Moon, Mars, Phobos, and Deimos with accurate orbital periods!")
    print("Use visibility controls to show/hide different celestial bodies and their trails.")
    create_earth_moon_sun_simulation()
