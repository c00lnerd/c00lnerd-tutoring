import tkinter as tk
import math

class Planet:
    def __init__(self, name, color, radius, distance, mass, velocity):
        self.name = name
        self.color = color
        self.radius = radius
        self.distance = distance
        self.mass = mass
        self.x = distance
        self.y = 0
        self.vx = 0
        self.vy = velocity
        self.trail = []

class SolarSystemSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar System Simulation")
        self.width = 900
        self.height = 850

        # ---- Layout ----
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="black", width=self.width, height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Control frame stays visible
        control_frame = tk.Frame(root, bg="#222222", height=40)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # ---- Physics ----
        self.G = 6.67430e-11
        self.scale = 1.5e9
        self.zoom_factor = 1.0
        self.time_step = 3600 * 12
        self.time_multiplier = 1.0

        # ---- Bodies ----
        self.sun = Planet("Sun", "yellow", 12, 0, 1.989e30, 0)
        self.earth = Planet("Earth", "deepskyblue", 6, 1.496e11, 5.972e24, 29783)
        self.mars = Planet("Mars", "orangered", 4, 2.279e11, 6.417e23, 24077)
        self.jupiter = Planet("Jupiter", "orange", 10, 7.785e11, 1.898e27, 13070)
        self.planets = [self.earth, self.mars, self.jupiter]
        self.running = True

        # ---- Controls ----
        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset, bg="gray20", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)

        tk.Label(control_frame, text="Simulation Speed:", fg="white", bg="#222222").pack(side=tk.LEFT, padx=5)
        self.speed_slider = tk.Scale(
            control_frame, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL,
            length=200, command=self.update_speed, fg="white", bg="#222222",
            highlightthickness=0, troughcolor="gray30"
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack(side=tk.LEFT, padx=5, pady=2)

        # ---- Bindings ----
        self.root.bind("<space>", self.toggle_simulation)
        self.root.bind("<MouseWheel>", self.zoom)
        self.root.bind("<Button-4>", self.zoom)  # Linux scroll up
        self.root.bind("<Button-5>", self.zoom)  # Linux scroll down

        self.animate()

    # ----- Control Methods -----
    def toggle_simulation(self, event=None):
        self.running = not self.running

    def zoom(self, event):
        if event.delta > 0 or getattr(event, "num", 0) == 4:
            self.zoom_factor *= 1.1
        elif event.delta < 0 or getattr(event, "num", 0) == 5:
            self.zoom_factor /= 1.1
        self.scale = 1.5e9 / self.zoom_factor

    def reset(self):
        for p in self.planets:
            p.trail.clear()
            p.x = p.distance
            p.y = 0
            p.vx = 0
            if p.name == "Earth":
                p.vy = 29783
            elif p.name == "Mars":
                p.vy = 24077
            elif p.name == "Jupiter":
                p.vy = 13070
        self.running = True

    def update_speed(self, val):
        self.time_multiplier = float(val)

    # ----- Physics -----
    def update_positions(self):
        bodies = [self.sun] + self.planets
        dt = self.time_step * self.time_multiplier

        for p in self.planets:
            ax = ay = 0
            for other in bodies:
                if p == other:
                    continue
                dx = other.x - p.x
                dy = other.y - p.y
                r = math.sqrt(dx**2 + dy**2)
                a = self.G * other.mass / r**2
                ax += a * dx / r
                ay += a * dy / r

            p.vx += ax * dt
            p.vy += ay * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.trail.append((p.x, p.y))
            if len(p.trail) > 1500:
                p.trail.pop(0)

    # ----- Drawing -----
    def draw(self):
        self.canvas.delete("all")
        cx, cy = self.width / 2, self.height / 2
        self.canvas.create_oval(cx - 12, cy - 12, cx + 12, cy + 12, fill="yellow")

        for p in self.planets:
            for i in range(1, len(p.trail)):
                x1 = cx + p.trail[i-1][0] / self.scale
                y1 = cy + p.trail[i-1][1] / self.scale
                x2 = cx + p.trail[i][0] / self.scale
                y2 = cy + p.trail[i][1] / self.scale
                self.canvas.create_line(x1, y1, x2, y2, fill=p.color, width=1)

            x = cx + p.x / self.scale
            y = cy + p.y / self.scale
            self.canvas.create_oval(x - p.radius, y - p.radius, x + p.radius, y + p.radius, fill=p.color)
            self.canvas.create_text(x + 15, y, text=p.name, fill=p.color, font=("Arial", 10))

    def animate(self):
        if self.running:
            self.update_positions()
        self.draw()
        self.root.after(20, self.animate)

# Run
root = tk.Tk()
app = SolarSystemSim(root)
root.mainloop()
