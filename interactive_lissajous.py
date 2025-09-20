import math
import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame
import time

def create_interactive_lissajous():
    """
    Interactive Lissajous curve generator with sliders
    Students can adjust frequency ratios, amplitude, and phase in real-time
    """
    root = tk.Tk()
    root.title("Interactive Lissajous Curve Explorer")
    root.geometry("1000x700")
    root.configure(bg='black')
    
    # Create main frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Canvas for drawing
    canvas = Canvas(main_frame, width=600, height=600, bg='black')
    canvas.pack(side=tk.LEFT, padx=(0, 20))
    
    # Control panel
    control_frame = Frame(main_frame, bg='black', width=300)
    control_frame.pack(side=tk.RIGHT, fill=tk.Y)
    control_frame.pack_propagate(False)
    
    # Title
    title_label = Label(control_frame, text="Lissajous Curve Controls", 
                       font=("Arial", 16, "bold"), fg="white", bg="black")
    title_label.pack(pady=(0, 20))
    
    # Variables for parameters
    freq_a = tk.DoubleVar(value=2.0)
    freq_b = tk.DoubleVar(value=3.0)
    amplitude_x = tk.DoubleVar(value=200.0)
    amplitude_y = tk.DoubleVar(value=200.0)
    phase_shift = tk.DoubleVar(value=0.0)
    speed = tk.DoubleVar(value=1.0)
    trail_length = tk.IntVar(value=500)
    
    # Create sliders
    def create_slider(parent, label, variable, from_, to, resolution=0.1):
        frame = Frame(parent, bg='black')
        frame.pack(fill=tk.X, pady=5)
        
        Label(frame, text=label, fg="white", bg="black", font=("Arial", 10, "bold")).pack()
        slider = Scale(frame, from_=from_, to=to, resolution=resolution, 
                      orient=tk.HORIZONTAL, variable=variable, 
                      bg="gray20", fg="white", highlightbackground="black",
                      activebackground="gray30", troughcolor="gray40")
        slider.pack(fill=tk.X)
        return slider
    
    # Frequency controls
    Label(control_frame, text="Frequency Ratios", fg="cyan", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(0, 10))
    
    freq_a_slider = create_slider(control_frame, "X Frequency (a)", freq_a, 0.1, 10.0, 0.1)
    freq_b_slider = create_slider(control_frame, "Y Frequency (b)", freq_b, 0.1, 10.0, 0.1)
    
    # Amplitude controls
    Label(control_frame, text="Amplitudes", fg="yellow", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    amp_x_slider = create_slider(control_frame, "X Amplitude", amplitude_x, 50, 250, 10)
    amp_y_slider = create_slider(control_frame, "Y Amplitude", amplitude_y, 50, 250, 10)
    
    # Phase and animation controls
    Label(control_frame, text="Animation", fg="lime", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(10, 10))
    
    phase_slider = create_slider(control_frame, "Phase Shift (δ)", phase_shift, 0, 6.28, 0.1)
    speed_slider = create_slider(control_frame, "Animation Speed", speed, 0.1, 3.0, 0.1)
    trail_slider = create_slider(control_frame, "Trail Length", trail_length, 50, 1000, 50)
    
    # Preset buttons
    Label(control_frame, text="Presets", fg="magenta", bg="black", 
          font=("Arial", 12, "bold")).pack(pady=(20, 10))
    
    preset_frame = Frame(control_frame, bg='black')
    preset_frame.pack(fill=tk.X)
    
    def set_preset(a, b, phase=0):
        freq_a.set(a)
        freq_b.set(b)
        phase_shift.set(phase)
        amplitude_x.set(200)
        amplitude_y.set(200)
    
    presets = [
        ("Circle", 1, 1, 1.57),
        ("Figure-8", 1, 2, 0),
        ("Flower", 3, 4, 0),
        ("Complex", 5, 6, 0)
    ]
    
    for i, (name, a, b, phase) in enumerate(presets):
        btn = tk.Button(preset_frame, text=name, 
                       command=lambda a=a, b=b, p=phase: set_preset(a, b, p),
                       bg="gray30", fg="white", font=("Arial", 8))
        btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
    
    preset_frame.grid_columnconfigure(0, weight=1)
    preset_frame.grid_columnconfigure(1, weight=1)
    
    # Drawing variables
    points_history = []
    start_time = time.time()
    
    def draw_frame():
        nonlocal points_history
        
        # Get current parameter values
        a = freq_a.get()
        b = freq_b.get()
        amp_x = amplitude_x.get()
        amp_y = amplitude_y.get()
        phase = phase_shift.get()
        anim_speed = speed.get()
        max_points = trail_length.get()
        
        # Animation time
        t = (time.time() - start_time) * anim_speed
        
        # Calculate current point
        x = 300 + amp_x * math.sin(a * t + phase)
        y = 300 + amp_y * math.sin(b * t)
        
        # Add to history
        points_history.append((x, y))
        
        # Limit trail length
        if len(points_history) > max_points:
            points_history.pop(0)
        
        # Clear canvas
        canvas.delete("all")
        
        # Draw the trail with fading effect
        if len(points_history) > 1:
            for i in range(1, len(points_history)):
                # Calculate fade factor
                fade = i / len(points_history)
                
                # Create color with fade
                r = int(255 * fade)
                g = int(100 + 155 * fade)
                b = int(200 * fade)
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                # Draw line segment
                x1, y1 = points_history[i-1]
                x2, y2 = points_history[i]
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        
        # Draw current point
        if points_history:
            curr_x, curr_y = points_history[-1]
            canvas.create_oval(curr_x-5, curr_y-5, curr_x+5, curr_y+5, 
                             fill="white", outline="yellow", width=2)
        
        # Draw center axes
        canvas.create_line(0, 300, 600, 300, fill="gray30", width=1)
        canvas.create_line(300, 0, 300, 600, fill="gray30", width=1)
        
        # Display current equation
        equation = f"x = {amp_x:.0f} × sin({a:.1f}t + {phase:.2f})"
        equation2 = f"y = {amp_y:.0f} × sin({b:.1f}t)"
        ratio = f"Frequency Ratio: {a:.1f}:{b:.1f}"
        
        canvas.create_text(300, 30, text="Lissajous Curve", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(300, 50, text=equation, 
                          fill="cyan", font=("Arial", 12))
        canvas.create_text(300, 70, text=equation2, 
                          fill="cyan", font=("Arial", 12))
        canvas.create_text(300, 90, text=ratio, 
                          fill="yellow", font=("Arial", 12))
        
        # Schedule next frame
        root.after(20, draw_frame)
    
    # Control buttons
    def reset_animation():
        nonlocal points_history, start_time
        points_history = []
        start_time = time.time()
    
    def clear_trail():
        nonlocal points_history
        points_history = []
    
    button_frame = Frame(control_frame, bg='black')
    button_frame.pack(pady=20)
    
    reset_btn = tk.Button(button_frame, text="Reset Animation", 
                         command=reset_animation, bg="red", fg="white", 
                         font=("Arial", 10, "bold"), width=12)
    reset_btn.pack(pady=2)
    
    clear_btn = tk.Button(button_frame, text="Clear Trail", 
                         command=clear_trail, bg="orange", fg="white", 
                         font=("Arial", 10, "bold"), width=12)
    clear_btn.pack(pady=2)
    
    # Instructions
    instructions = [
        "• Adjust sliders to see real-time changes",
        "• Use 'Clear Trail' to see immediate effects",
        "• Try different frequency ratios",
        "• Use presets for classic patterns",
        "• Watch how phase shift affects shape",
        "• Experiment with amplitudes"
    ]
    
    Label(control_frame, text="Instructions:", fg="orange", bg="black", 
          font=("Arial", 10, "bold")).pack(pady=(20, 5))
    
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
    create_interactive_lissajous()
