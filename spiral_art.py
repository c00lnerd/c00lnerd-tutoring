import math
import tkinter as tk
from tkinter import Canvas
import time

def create_spiral_art():
    """
    Creates an animated mathematical spiral art visualization
    Perfect for demonstrating trigonometry, loops, and animation concepts
    """
    root = tk.Tk()
    root.title("Mathematical Spiral Art")
    root.geometry("800x600")
    root.configure(bg='black')
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    def draw_frame():
        canvas.delete("all")
        
        # Animation time parameter
        t = time.time()
        
        # Center of the canvas
        center_x, center_y = 400, 300
        
        # Draw multiple spirals with different parameters
        for spiral in range(8):
            points = []
            
            # Calculate spiral points
            for angle in range(0, 720, 2):  # Two full rotations
                # Convert angle to radians
                rad = math.radians(angle)
                
                # Spiral radius grows with angle
                radius = angle / 10 + 20
                
                # Add time-based rotation and spiral offset
                x = center_x + radius * math.cos(rad + t + spiral * math.pi/4)
                y = center_y + radius * math.sin(rad + t + spiral * math.pi/4)
                
                points.extend([x, y])
            
            # Create gradient color based on spiral number
            hue = (spiral * 45 + t * 50) % 360
            r = int(127 * (1 + math.sin(math.radians(hue))))
            g = int(127 * (1 + math.sin(math.radians(hue + 120))))
            b = int(127 * (1 + math.sin(math.radians(hue + 240))))
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw the spiral as a smooth line
            if len(points) >= 4:
                canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Add some decorative elements
        for i in range(12):
            angle = i * 30 + t * 20
            rad = math.radians(angle)
            x = center_x + 150 * math.cos(rad)
            y = center_y + 150 * math.sin(rad)
            
            # Pulsing circles
            size = 10 + 5 * math.sin(t * 3 + i)
            canvas.create_oval(x-size, y-size, x+size, y+size, 
                             fill="white", outline="yellow", width=2)
        
        # Schedule next frame (60 FPS)
        root.after(16, draw_frame)
    
    # Add instructions
    canvas.create_text(400, 50, text="Mathematical Spiral Art", 
                      fill="white", font=("Arial", 20, "bold"))
    canvas.create_text(400, 80, text="Press ESC to exit", 
                      fill="gray", font=("Arial", 12))
    
    # Bind escape key to close
    def on_escape(event):
        root.quit()
    
    root.bind('<Escape>', on_escape)
    root.focus_set()
    
    # Start animation
    draw_frame()
    root.mainloop()

if __name__ == "__main__":
    create_spiral_art()
