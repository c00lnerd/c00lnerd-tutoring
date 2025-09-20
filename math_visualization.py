import math
import tkinter as tk
from tkinter import Canvas
import time

# Mathematical visualization code
def create_visualization():
    root = tk.Tk()
    root.title("Mathematical Visualization")
    root.geometry("800x600")
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    def animate():
        canvas.delete("all")
        
        # Get current time for animation
        t = time.time() * 2
        
        # Mathematical parameters
        a = (400, 300, 0)  # Center point
        mag = lambda k: k * 8 / 8 - 12
        e = 0
        d = 5
        
        # Draw mathematical pattern
        for k in range(-12, 12):
            for i in range(0, 360, 5):
                x = a[0] + mag(k) * math.cos(math.radians(i + t))
                y = a[1] + mag(k) * math.sin(math.radians(i + t))
                
                # Create colorful points
                color_val = int(255 * (math.sin(i/10 + t) + 1) / 2)
                color = f"#{color_val:02x}{(255-color_val):02x}80"
                
                canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline="")
        
        # Schedule next frame
        root.after(50, animate)
    
    animate()
    root.mainloop()

if __name__ == "__main__":
    create_visualization()
