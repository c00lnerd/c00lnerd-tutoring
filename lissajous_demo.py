import math
import tkinter as tk
from tkinter import Canvas
import time

def create_lissajous_art():
    """
    Creates animated Lissajous curve patterns
    Lissajous curves are created by parametric equations:
    x = A * sin(a*t + δ)
    y = B * sin(b*t)
    """
    root = tk.Tk()
    root.title("Lissajous Curve Art")
    root.geometry("800x600")
    root.configure(bg='black')
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    def draw_frame():
        canvas.delete("all")
        
        # Animation time parameter
        t = time.time() * 0.5
        
        # Center of the canvas
        center_x, center_y = 400, 300
        
        # Draw multiple Lissajous curves with different frequency ratios
        curves = [
            {"a": 2, "b": 3, "scale": 80, "color_offset": 0},
            {"a": 3, "b": 4, "scale": 60, "color_offset": 60},
            {"a": 4, "b": 5, "scale": 100, "color_offset": 120},
            {"a": 5, "b": 6, "scale": 70, "color_offset": 180},
            {"a": 1, "b": 2, "scale": 90, "color_offset": 240},
        ]
        
        for curve_params in curves:
            points = []
            a = curve_params["a"]
            b = curve_params["b"]
            scale = curve_params["scale"]
            
            # Calculate Lissajous curve points
            for i in range(0, 628, 1):  # 0 to 2π * 100
                param = i / 100.0  # Parameter from 0 to 2π
                
                # Classic Lissajous equations with time animation
                x = center_x + scale * math.sin(a * param + t)
                y = center_y + scale * math.sin(b * param + t * 0.7)
                
                points.extend([x, y])
            
            # Create rainbow colors
            hue = (curve_params["color_offset"] + t * 30) % 360
            r = int(127 * (1 + math.sin(math.radians(hue))))
            g = int(127 * (1 + math.sin(math.radians(hue + 120))))
            b = int(127 * (1 + math.sin(math.radians(hue + 240))))
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw the curve
            if len(points) >= 4:
                canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Add mathematical formula display
        canvas.create_text(400, 30, text="Lissajous Curves: x = sin(at + φ), y = sin(bt + ψ)", 
                          fill="white", font=("Arial", 14, "bold"))
        canvas.create_text(400, 50, text="Different frequency ratios create different patterns", 
                          fill="cyan", font=("Arial", 12))
        
        # Show current frequency ratios
        canvas.create_text(100, 570, text="Ratios: 2:3, 3:4, 4:5, 5:6, 1:2", 
                          fill="yellow", font=("Arial", 10))
        
        # Schedule next frame
        root.after(50, draw_frame)
    
    # Bind escape key to close
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    create_lissajous_art()
