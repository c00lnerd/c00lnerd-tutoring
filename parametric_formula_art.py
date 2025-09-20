import math
import tkinter as tk
from tkinter import Canvas
import time

def create_parametric_formula_art():
    """
    Creates mathematical art based on the complex parametric formula from the image
    This appears to be a sophisticated mathematical curve with multiple harmonics
    """
    root = tk.Tk()
    root.title("Parametric Formula Art")
    root.geometry("800x600")
    root.configure(bg='black')
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    def draw_formula_art():
        canvas.delete("all")
        
        # Center the drawing
        center_x, center_y = 400, 300
        scale = 150  # Scale factor to make the pattern visible
        
        # Draw the parametric curve based on the formula
        points = []
        
        # The formula appears to be:
        # a = (x, y, d=mag(k=11*cos(x/8), e=y/8-12.5)*x3/1499+cos(e/4+t*2)/5+1)
        # This looks like a complex parametric equation with time animation
        
        current_time = time.time() * 0.5  # Slow down the animation
        
        # Generate points along the curve
        for t in range(0, 3600, 2):  # 0 to 360 degrees * 10 for more detail
            t_rad = math.radians(t / 10)  # Convert to radians and scale
            
            # Reconstruct the formula from the image
            # This appears to be a complex parametric curve
            k = 11 * math.cos(t_rad / 8)
            e = t_rad / 8 - 12.5
            
            # Complex mathematical expression
            mag_component = e * 3 / 1499 + math.cos(e / 4 + current_time * 2) / 5 + 1
            
            # Additional harmonic components
            d = k * (3 + math.sin(t_rad + current_time * 2)) * math.sin(mag_component / 
                     (e / 99 + t_rad / 99 + math.cos(mag_component) + 200))
            
            # Calculate x and y coordinates
            x = center_x + scale * d * math.cos(t_rad)
            y = center_y + scale * d * math.sin(t_rad)
            
            # Keep points on screen
            if 0 <= x <= 800 and 0 <= y <= 600:
                points.append((x, y))
        
        # Draw the curve with gradient colors
        if len(points) > 1:
            for i in range(1, len(points)):
                # Create color gradient
                progress = i / len(points)
                
                # Rainbow effect
                hue = (progress * 360 + current_time * 50) % 360
                r = int(127 * (1 + math.sin(math.radians(hue))))
                g = int(127 * (1 + math.sin(math.radians(hue + 120))))
                b = int(127 * (1 + math.sin(math.radians(hue + 240))))
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                x1, y1 = points[i-1]
                x2, y2 = points[i]
                
                # Vary line width based on position
                width = max(1, int(3 * (1 + math.sin(progress * math.pi * 4))))
                
                canvas.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)
        
        # Add some decorative elements
        # Draw center point
        canvas.create_oval(center_x-3, center_y-3, center_x+3, center_y+3, 
                          fill="white", outline="yellow", width=2)
        
        # Add title and info
        canvas.create_text(400, 30, text="Parametric Formula Art", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(400, 50, text="Complex Mathematical Curve with Harmonics", 
                          fill="cyan", font=("Arial", 12))
        
        # Show the mathematical formula (simplified)
        canvas.create_text(400, 570, text="Formula: d = k(3+sin(t+τ))×sin(mag/(e/99+t/99+cos(mag)+200))", 
                          fill="yellow", font=("Arial", 10))
        
        # Schedule next frame
        root.after(50, draw_formula_art)
    
    # Bind escape key to close
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    # Start animation
    draw_formula_art()
    root.mainloop()

def create_enhanced_parametric_art():
    """
    Enhanced version with multiple variations of the formula
    """
    root = tk.Tk()
    root.title("Enhanced Parametric Formula Art")
    root.geometry("800x600")
    root.configure(bg='black')
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    def draw_enhanced_art():
        canvas.delete("all")
        
        center_x, center_y = 400, 300
        current_time = time.time() * 0.3
        
        # Draw multiple variations of the formula with much larger scales
        variations = [
            {"scale": 200, "color_offset": 0, "time_mult": 1, "amplitude": 1.5},
            {"scale": 160, "color_offset": 120, "time_mult": 1.5, "amplitude": 1.2},
            {"scale": 240, "color_offset": 240, "time_mult": 0.7, "amplitude": 1.8}
        ]
        
        for var in variations:
            points = []
            scale = var["scale"]
            
            for t in range(0, 3600, 3):
                t_rad = math.radians(t / 10)
                
                # Enhanced formula with variations
                k = 11 * math.cos(t_rad / 8 + current_time * var["time_mult"]) * var["amplitude"]
                e = t_rad / 8 - 12.5 + math.sin(current_time * 0.5) * 2
                
                # More complex magnitude calculation with amplitude boost
                mag_component = (e * 3 / 1499 + 
                               math.cos(e / 4 + current_time * 2 * var["time_mult"]) / 5 + 
                               math.sin(t_rad * 0.1 + current_time) * 0.3 + 1) * var["amplitude"]
                
                # Enhanced distance calculation with larger amplitude
                d = k * (3 + math.sin(t_rad + current_time * 2 * var["time_mult"])) * \
                    math.sin(mag_component / (e / 99 + t_rad / 99 + math.cos(mag_component) + 200)) * var["amplitude"]
                
                # Add some noise for organic feel
                noise_x = math.sin(t_rad * 3 + current_time * 1.5) * 5
                noise_y = math.cos(t_rad * 2.7 + current_time * 1.2) * 5
                
                x = center_x + scale * d * math.cos(t_rad) + noise_x
                y = center_y + scale * d * math.sin(t_rad) + noise_y
                
                if 0 <= x <= 800 and 0 <= y <= 600:
                    points.append((x, y))
            
            # Draw this variation
            if len(points) > 1:
                for i in range(1, len(points)):
                    progress = i / len(points)
                    
                    # Color with variation offset
                    hue = (progress * 360 + current_time * 30 + var["color_offset"]) % 360
                    r = int(127 * (1 + math.sin(math.radians(hue))))
                    g = int(127 * (1 + math.sin(math.radians(hue + 120))))
                    b = int(127 * (1 + math.sin(math.radians(hue + 240))))
                    
                    # Fade based on variation
                    alpha = 0.7 if var == variations[0] else 0.5
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    x1, y1 = points[i-1]
                    x2, y2 = points[i]
                    
                    width = max(1, int(2 * (1 + math.sin(progress * math.pi * 6))))
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        
        # Decorative center
        pulse = 5 + 3 * math.sin(current_time * 3)
        canvas.create_oval(center_x-pulse, center_y-pulse, center_x+pulse, center_y+pulse, 
                          fill="white", outline="gold", width=2)
        
        # Title and info
        canvas.create_text(400, 25, text="Enhanced Parametric Formula Art", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(400, 45, text="Multiple Harmonic Variations", 
                          fill="cyan", font=("Arial", 12))
        
        # Mathematical description
        canvas.create_text(400, 575, text="Multi-layered parametric equations with time-varying harmonics", 
                          fill="yellow", font=("Arial", 10))
        
        root.after(40, draw_enhanced_art)
    
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    draw_enhanced_art()
    root.mainloop()

if __name__ == "__main__":
    print("Choose version:")
    print("1. Basic Parametric Formula Art")
    print("2. Enhanced Multi-layer Version")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        create_enhanced_parametric_art()
    else:
        create_parametric_formula_art()
