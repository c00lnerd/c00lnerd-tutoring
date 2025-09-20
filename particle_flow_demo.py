import math
import tkinter as tk
from tkinter import Canvas
import time
import random

def create_particle_flow():
    """
    Creates a beautiful particle flow visualization similar to the image
    Features flowing particles along curved paths with trails
    """
    root = tk.Tk()
    root.title("Particle Flow Visualization")
    root.geometry("800x600")
    root.configure(bg='black')
    
    canvas = Canvas(root, width=800, height=600, bg='black')
    canvas.pack()
    
    # Particle system
    particles = []
    flow_lines = []
    
    class Particle:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            self.life = random.uniform(100, 200)
            self.max_life = self.life
            self.size = random.uniform(1, 3)
            self.trail = []
            
        def update(self, center_x, center_y, t):
            # Create flow field effect - particles flow around center
            dx = self.x - center_x
            dy = self.y - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Create swirling motion
                angle = math.atan2(dy, dx)
                flow_angle = angle + math.pi/2 + math.sin(t * 0.01 + distance * 0.01) * 0.5
                
                # Flow strength decreases with distance
                flow_strength = max(0, 200 - distance) / 200
                
                self.vx += math.cos(flow_angle) * flow_strength * 0.1
                self.vy += math.sin(flow_angle) * flow_strength * 0.1
            
            # Add some randomness
            self.vx += random.uniform(-0.1, 0.1)
            self.vy += random.uniform(-0.1, 0.1)
            
            # Limit velocity
            speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
            if speed > 3:
                self.vx = (self.vx / speed) * 3
                self.vy = (self.vy / speed) * 3
            
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Add to trail
            self.trail.append((self.x, self.y))
            if len(self.trail) > 20:
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
                
            # Draw trail
            for i in range(1, len(self.trail)):
                fade = (i / len(self.trail)) * (self.life / self.max_life)
                alpha = int(255 * fade)
                
                # Create blue-white gradient
                r = int(100 + 155 * fade)
                g = int(150 + 105 * fade)
                b = 255
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                x1, y1 = self.trail[i-1]
                x2, y2 = self.trail[i]
                
                canvas.create_line(x1, y1, x2, y2, fill=color, width=max(1, int(fade * 2)))
            
            # Draw particle
            if self.trail:
                fade = self.life / self.max_life
                size = self.size * fade
                x, y = self.trail[-1]
                
                # Bright center
                canvas.create_oval(x-size, y-size, x+size, y+size, 
                                 fill="white", outline="cyan", width=1)
    
    def create_flow_field(center_x, center_y, t):
        """Create flowing field lines"""
        field_lines = []
        
        for angle in range(0, 360, 15):
            points = []
            rad = math.radians(angle)
            
            # Start from center and flow outward
            for r in range(10, 300, 5):
                # Create spiral flow
                flow_angle = rad + r * 0.02 + math.sin(t * 0.001 + r * 0.01) * 0.3
                x = center_x + r * math.cos(flow_angle)
                y = center_y + r * math.sin(flow_angle)
                
                if 0 <= x <= 800 and 0 <= y <= 600:
                    points.append((x, y))
            
            if len(points) > 1:
                field_lines.append(points)
        
        return field_lines
    
    def draw_frame():
        canvas.delete("all")
        
        current_time = time.time() * 1000  # Convert to milliseconds
        
        # Center point with some movement
        center_x = 400 + 50 * math.sin(current_time * 0.001)
        center_y = 300 + 30 * math.cos(current_time * 0.0015)
        
        # Draw flow field lines (faint)
        flow_lines = create_flow_field(center_x, center_y, current_time)
        for line in flow_lines:
            if len(line) > 1:
                # Draw faint flow lines
                for i in range(1, len(line)):
                    fade = (len(line) - i) / len(line)
                    alpha = int(50 * fade)
                    color = f"#{alpha:02x}{alpha:02x}{alpha+50:02x}"
                    
                    x1, y1 = line[i-1]
                    x2, y2 = line[i]
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
        
        # Add new particles occasionally
        if random.random() < 0.1:
            # Spawn particles around the center
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 150)
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            particles.append(Particle(x, y))
        
        # Update and draw particles
        for particle in particles[:]:
            particle.update(center_x, center_y, current_time)
            if particle.life <= 0:
                particles.remove(particle)
            else:
                particle.draw(canvas)
        
        # Draw center attraction point
        pulse = 5 + 3 * math.sin(current_time * 0.005)
        canvas.create_oval(center_x-pulse, center_y-pulse, 
                          center_x+pulse, center_y+pulse, 
                          fill="white", outline="cyan", width=2)
        
        # Add some background stars
        for _ in range(20):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            brightness = random.randint(50, 150)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            canvas.create_oval(x, y, x+1, y+1, fill=color, outline="")
        
        # Title
        canvas.create_text(400, 30, text="Particle Flow Visualization", 
                          fill="white", font=("Arial", 16, "bold"))
        canvas.create_text(400, 50, text="Press ESC to exit", 
                          fill="gray", font=("Arial", 10))
        
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
    create_particle_flow()
