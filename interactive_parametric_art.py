import math
import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame
import time

def create_interactive_parametric_art():
    """
    Interactive parametric formula art with much larger patterns and parameter controls
    """
    root = tk.Tk()
    root.title("Interactive Parametric Formula Art")
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
    title_label = Label(control_frame, text="Parametric Formula Controls", 
                       font=("Arial", 16, "bold"), fg="white", bg="black")
    title_label.pack(pady=(0, 20))
    
    # Parameters with much more aggressive scaling
    scale_factor = tk.DoubleVar(value=300.0)  # Much larger base scale
    k_multiplier = tk.DoubleVar(value=15.0)   # Boost the k parameter
    time_speed = tk.DoubleVar(value=1.0)
    pattern_complexity = tk.DoubleVar(value=1.0)
    amplitude_boost = tk.DoubleVar(value=5.0)  # Major amplitude boost
    harmonic_layers = tk.IntVar(value=3)
    line_width = tk.DoubleVar(value=2.0)
    
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
    
    # Scale Controls
    Label(control_frame, text="Size & Scale", fg="cyan", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(0, 10))
    
    create_slider(control_frame, "Scale Factor", scale_factor, 50, 500, 10)
    create_slider(control_frame, "K Multiplier", k_multiplier, 5, 30, 1)
    create_slider(control_frame, "Amplitude Boost", amplitude_boost, 1, 20, 0.5)
    
    # Pattern Controls
    Label(control_frame, text="Pattern Dynamics", fg="yellow", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    create_slider(control_frame, "Time Speed", time_speed, 0.1, 3.0, 0.1)
    create_slider(control_frame, "Complexity", pattern_complexity, 0.5, 3.0, 0.1)
    create_slider(control_frame, "Harmonic Layers", harmonic_layers, 1, 5, 1)
    
    # Visual Controls
    Label(control_frame, text="Visual Effects", fg="lime", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    create_slider(control_frame, "Line Width", line_width, 1, 5, 0.5)
    
    def draw_frame():
        canvas.delete("all")
        
        center_x, center_y = 400, 300
        current_time = time.time() * time_speed.get()
        
        # Get current parameters
        scale = scale_factor.get()
        k_mult = k_multiplier.get()
        complexity = pattern_complexity.get()
        amp_boost = amplitude_boost.get()
        layers = harmonic_layers.get()
        width = line_width.get()
        
        # Draw multiple harmonic layers
        for layer in range(layers):
            points = []
            layer_offset = layer * 0.3
            layer_scale = scale * (1 - layer * 0.1)  # Slightly different scales
            
            # Much denser point generation for smoother curves
            for t in range(0, 3600, 1):  # More points for smoother curves
                t_rad = math.radians(t / 10)
                
                # Enhanced formula with MUCH larger values
                k = k_mult * math.cos(t_rad / 8 + current_time + layer_offset) * complexity
                e = t_rad / 8 - 12.5 + math.sin(current_time * 0.5) * 2
                
                # Magnitude calculation with major boost
                mag_component = (e * 3 / 1499 + 
                               math.cos(e / 4 + current_time * 2) / 5 + 
                               math.sin(t_rad * 0.1 + current_time) * 0.3 + 1) * amp_boost
                
                # Distance calculation with massive amplitude boost
                try:
                    denominator = e / 99 + t_rad / 99 + math.cos(mag_component) + 200
                    if abs(denominator) > 0.001:  # Avoid division by zero
                        d = k * (3 + math.sin(t_rad + current_time * 2)) * \
                            math.sin(mag_component / denominator) * amp_boost
                    else:
                        d = 0
                except:
                    d = 0
                
                # Calculate final position with huge scale
                x = center_x + layer_scale * d * math.cos(t_rad)
                y = center_y + layer_scale * d * math.sin(t_rad)
                
                # Keep reasonable bounds but allow large patterns
                if -200 <= x - center_x <= 200 and -200 <= y - center_y <= 200:
                    points.append((x, y))
            
            # Draw this layer
            if len(points) > 1:
                for i in range(1, len(points)):
                    progress = i / len(points)
                    
                    # Layer-specific colors
                    hue = (progress * 360 + current_time * 30 + layer * 72) % 360
                    r = int(127 * (1 + math.sin(math.radians(hue))))
                    g = int(127 * (1 + math.sin(math.radians(hue + 120))))
                    b = int(127 * (1 + math.sin(math.radians(hue + 240))))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    x1, y1 = points[i-1]
                    x2, y2 = points[i]
                    
                    # Variable line width
                    current_width = max(1, int(width * (1 + math.sin(progress * math.pi * 4) * 0.5)))
                    
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=current_width, smooth=True)
        
        # Enhanced center point
        pulse = 8 + 5 * math.sin(current_time * 3)
        canvas.create_oval(center_x-pulse, center_y-pulse, center_x+pulse, center_y+pulse, 
                          fill="white", outline="gold", width=3)
        
        # Info display
        canvas.create_text(400, 25, text="Interactive Parametric Formula Art", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(400, 45, text=f"Scale: {scale:.0f} | Layers: {layers} | Complexity: {complexity:.1f}", 
                          fill="cyan", font=("Arial", 12))
        
        # Mathematical formula
        canvas.create_text(400, 575, text="d = k(3+sin(t+τ))×sin(mag/(e/99+t/99+cos(mag)+200)) × BOOST", 
                          fill="yellow", font=("Arial", 10))
        
        # Schedule next frame
        root.after(30, draw_frame)
    
    # Control buttons
    def reset_defaults():
        scale_factor.set(300.0)
        k_multiplier.set(15.0)
        time_speed.set(1.0)
        pattern_complexity.set(1.0)
        amplitude_boost.set(5.0)
        harmonic_layers.set(3)
        line_width.set(2.0)
    
    def preset_large():
        scale_factor.set(400.0)
        k_multiplier.set(25.0)
        amplitude_boost.set(10.0)
        pattern_complexity.set(2.0)
        harmonic_layers.set(4)
    
    def preset_complex():
        scale_factor.set(350.0)
        k_multiplier.set(20.0)
        amplitude_boost.set(8.0)
        pattern_complexity.set(2.5)
        harmonic_layers.set(5)
        time_speed.set(0.5)
    
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Reset Defaults", command=reset_defaults,
              bg="red", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=2)
    
    tk.Button(button_frame, text="Large Pattern", command=preset_large,
              bg="orange", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=2)
    
    tk.Button(button_frame, text="Complex Pattern", command=preset_complex,
              bg="purple", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=2)
    
    # Instructions
    Label(control_frame, text="Instructions:", fg="orange", bg="black", 
          font=("Arial", 10, "bold")).pack(pady=(20, 5))
    
    instructions = [
        "• Use Scale Factor for overall size",
        "• K Multiplier affects pattern shape",
        "• Amplitude Boost makes patterns larger",
        "• Try the preset buttons for dramatic effects",
        "• Adjust layers for complexity"
    ]
    
    for instruction in instructions:
        Label(control_frame, text=instruction, fg="white", bg="black", 
              font=("Arial", 8), anchor="w").pack(anchor="w", padx=10)
    
    # Bind escape key to close
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    create_interactive_parametric_art()
