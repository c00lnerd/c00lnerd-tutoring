import math
import tkinter as tk
from tkinter import Canvas, Label, Frame
import time
import random

class GameObject:
    """Base class for all game objects"""
    def __init__(self, x, y, vx=0, vy=0, radius=5, color="white"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.alive = True
    
    def update(self, dt):
        """Update position based on velocity"""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def draw(self, canvas):
        """Draw the object"""
        canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, outline="white"
        )

class Planet(GameObject):
    """A planet with gravitational effects"""
    def __init__(self, x, y, vx, vy, mass, color, planet_type="normal"):
        radius = max(8, math.sqrt(mass) * 1.2)
        super().__init__(x, y, vx, vy, radius, color)
        self.mass = mass
        self.planet_type = planet_type
        self.trail = []
        self.points = int(mass / 10)  # Points based on mass
    
    def update(self, dt):
        super().update(dt)
        # Add to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:
            self.trail.pop(0)
    
    def draw(self, canvas):
        # Draw trail
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                fade = i / len(self.trail)
                alpha = int(255 * fade * 0.3)
                x1, y1 = self.trail[i-1]
                x2, y2 = self.trail[i]
                canvas.create_line(x1, y1, x2, y2, fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}", width=1)
        
        # Draw planet with special effects
        if self.planet_type == "fuel":
            # Pulsing green fuel depot
            pulse = 1 + 0.3 * math.sin(time.time() * 5)
            canvas.create_oval(
                self.x - self.radius * pulse, self.y - self.radius * pulse,
                self.x + self.radius * pulse, self.y + self.radius * pulse,
                fill=self.color, outline="lime", width=2
            )
        elif self.planet_type == "explosive":
            # Red explosive planet
            canvas.create_oval(
                self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius,
                fill=self.color, outline="red", width=2
            )
        else:
            # Normal planet
            super().draw(canvas)

class Spaceship(GameObject):
    """Player-controlled spaceship"""
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 8, "cyan")
        self.angle = 0  # Ship orientation
        self.thrust_power = 200
        self.fuel = 100
        self.max_fuel = 100
        self.shield = False
        self.shield_time = 0
        self.invulnerable_time = 0
    
    def apply_thrust(self, dt):
        """Apply thrust in the direction the ship is facing"""
        if self.fuel > 0:
            thrust_x = math.cos(self.angle) * self.thrust_power * dt
            thrust_y = math.sin(self.angle) * self.thrust_power * dt
            self.vx += thrust_x
            self.vy += thrust_y
            self.fuel -= 20 * dt
            self.fuel = max(0, self.fuel)
            return True
        return False
    
    def rotate(self, direction, dt):
        """Rotate the ship"""
        self.angle += direction * 3 * dt
    
    def update(self, dt):
        super().update(dt)
        # Update shield and invulnerability
        if self.shield_time > 0:
            self.shield_time -= dt
            self.shield = self.shield_time > 0
        if self.invulnerable_time > 0:
            self.invulnerable_time -= dt
    
    def draw(self, canvas):
        # Draw ship as a triangle pointing in the direction of movement
        size = self.radius
        # Calculate triangle points
        tip_x = self.x + size * math.cos(self.angle)
        tip_y = self.y + size * math.sin(self.angle)
        
        left_x = self.x + size * 0.6 * math.cos(self.angle + 2.5)
        left_y = self.y + size * 0.6 * math.sin(self.angle + 2.5)
        
        right_x = self.x + size * 0.6 * math.cos(self.angle - 2.5)
        right_y = self.y + size * 0.6 * math.sin(self.angle - 2.5)
        
        # Draw shield if active
        if self.shield:
            canvas.create_oval(
                self.x - size * 1.5, self.y - size * 1.5,
                self.x + size * 1.5, self.y + size * 1.5,
                outline="blue", width=2
            )
        
        # Draw ship (flashing if invulnerable)
        if self.invulnerable_time <= 0 or int(time.time() * 10) % 2:
            canvas.create_polygon(
                tip_x, tip_y, left_x, left_y, right_x, right_y,
                fill=self.color, outline="white"
            )

class Bullet(GameObject):
    """Projectile fired by the spaceship"""
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy, 2, "yellow")
        self.lifetime = 3.0  # Bullets disappear after 3 seconds
    
    def update(self, dt):
        super().update(dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

class GravitationalDestroyer:
    """Main game class"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gravitational Destroyer")
        self.root.geometry("1000x700")
        self.root.configure(bg='black')
        
        # Game state
        self.level = 1
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.level_complete = False
        
        # Physics constants
        self.G = 300
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Game objects
        self.spaceship = None
        self.planets = []
        self.bullets = []
        
        # Controls
        self.keys_pressed = set()
        
        self.setup_ui()
        self.start_level()
        self.bind_controls()
        
    def setup_ui(self):
        """Setup the game UI"""
        main_frame = Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game canvas
        self.canvas = Canvas(main_frame, width=self.canvas_width, height=self.canvas_height, bg='#000011')
        self.canvas.pack(side=tk.LEFT, padx=(0, 20))
        
        # Info panel
        info_frame = Frame(main_frame, bg='black', width=200)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        info_frame.pack_propagate(False)
        
        # Game info labels
        Label(info_frame, text="GRAVITATIONAL\nDESTROYER", fg="cyan", bg="black", 
              font=("Arial", 11, "bold"), justify="center").pack(pady=10)
        
        self.level_label = Label(info_frame, text="Level: 1", fg="white", bg="black", font=("Arial", 10))
        self.level_label.pack()
        
        self.score_label = Label(info_frame, text="Score: 0", fg="white", bg="black", font=("Arial", 10))
        self.score_label.pack()
        
        self.lives_label = Label(info_frame, text="Lives: 3", fg="white", bg="black", font=("Arial", 10))
        self.lives_label.pack()
        
        self.fuel_label = Label(info_frame, text="Fuel: 100%", fg="white", bg="black", font=("Arial", 10))
        self.fuel_label.pack()
        
        # Instructions
        Label(info_frame, text="\nCONTROLS:", fg="yellow", bg="black", 
              font=("Arial", 10, "bold")).pack(pady=(20, 5))
        
        instructions = [
            "Arrow Keys: Rotate & Thrust",
            "SPACE: Shoot",
            "P: Pause",
            "R: Restart Level",
            "",
            "OBJECTIVES:",
            "• Destroy all planets",
            "• Avoid collisions",
            "• Use gravity strategically",
            "• Collect fuel (green planets)",
            "",
            "PLANET TYPES:",
            "🟢 Fuel Depot (+fuel)",
            "🔴 Explosive (chain reaction)",
            "⚪ Normal (points)"
        ]
        
        for instruction in instructions:
            Label(info_frame, text=instruction, fg="white", bg="black", 
                  font=("Arial", 8), anchor="w").pack(anchor="w", padx=5)
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)
        self.root.focus_set()
    
    def key_press(self, event):
        """Handle key press events"""
        self.keys_pressed.add(event.keysym)
        
        if event.keysym == 'space':
            self.shoot()
        elif event.keysym == 'p':
            self.paused = not self.paused
        elif event.keysym == 'r':
            if self.game_over:
                self.restart_game()
            else:
                self.restart_level()
    
    def key_release(self, event):
        """Handle key release events"""
        self.keys_pressed.discard(event.keysym)
    
    def start_level(self):
        """Initialize a new level"""
        self.level_complete = False
        
        # Create spaceship at center
        self.spaceship = Spaceship(self.canvas_width // 2, self.canvas_height // 2)
        
        # Clear existing objects
        self.planets = []
        self.bullets = []
        
        # Calculate number of planets for this level
        num_planets = 3 + (self.level - 1) * 2  # 3, 5, 7, 9, 11...
        if self.level > 5:
            num_planets = 3 + (self.level - 1) * 5  # After level 5: 3, 5, 10, 15, 20...
        
        # Create planets
        for i in range(num_planets):
            self.create_random_planet()
        
        # Add special planets based on level
        if self.level >= 2:
            self.add_fuel_depot()
        if self.level >= 3:
            self.add_explosive_planet()
    
    def create_random_planet(self):
        """Create a random planet"""
        # Ensure planets don't spawn too close to the spaceship
        while True:
            x = random.randint(50, self.canvas_width - 50)
            y = random.randint(50, self.canvas_height - 50)
            
            # Check distance from spaceship
            if self.spaceship:
                dist = math.sqrt((x - self.spaceship.x)**2 + (y - self.spaceship.y)**2)
                if dist > 100:  # Minimum safe distance
                    break
        
        # Random orbital velocity
        center_x, center_y = self.canvas_width // 2, self.canvas_height // 2
        dx = x - center_x
        dy = y - center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            orbital_speed = 20 + random.random() * 30
            vx = -dy / distance * orbital_speed
            vy = dx / distance * orbital_speed
        else:
            vx = vy = 0
        
        mass = 50 + random.random() * 100
        colors = ['#ff6b6b', '#4ecdc4', '#ffbe0b', '#a3f7bf', '#7d53de', '#f7d6e0']
        color = random.choice(colors)
        
        planet = Planet(x, y, vx, vy, mass, color)
        self.planets.append(planet)
    
    def add_fuel_depot(self):
        """Add a fuel depot planet"""
        x = random.randint(100, self.canvas_width - 100)
        y = random.randint(100, self.canvas_height - 100)
        
        planet = Planet(x, y, 0, 0, 80, "#00ff00", "fuel")
        self.planets.append(planet)
    
    def add_explosive_planet(self):
        """Add an explosive planet"""
        x = random.randint(100, self.canvas_width - 100)
        y = random.randint(100, self.canvas_height - 100)
        
        planet = Planet(x, y, 0, 0, 120, "#ff0000", "explosive")
        self.planets.append(planet)
    
    def shoot(self):
        """Fire a bullet from the spaceship"""
        if not self.spaceship or self.game_over or self.paused:
            return
        
        # Bullet starts at ship position with ship velocity + bullet velocity
        bullet_speed = 300
        bullet_vx = self.spaceship.vx + bullet_speed * math.cos(self.spaceship.angle)
        bullet_vy = self.spaceship.vy + bullet_speed * math.sin(self.spaceship.angle)
        
        bullet = Bullet(self.spaceship.x, self.spaceship.y, bullet_vx, bullet_vy)
        self.bullets.append(bullet)
    
    def restart_level(self):
        """Restart the current level"""
        self.start_level()
    
    def restart_game(self):
        """Restart the entire game from level 1"""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.level_complete = False
        self.start_level()
    
    def next_level(self):
        """Advance to the next level"""
        self.level += 1
        self.start_level()
    
    def apply_gravity(self, dt):
        """Apply gravitational forces to all objects"""
        all_objects = [self.spaceship] + self.bullets
        
        for obj in all_objects:
            if not obj or not obj.alive:
                continue
                
            # Reset acceleration
            ax = ay = 0
            
            # Calculate gravitational force from each planet
            for planet in self.planets:
                if not planet.alive:
                    continue
                    
                dx = planet.x - obj.x
                dy = planet.y - obj.y
                distance_sq = dx*dx + dy*dy
                distance = math.sqrt(distance_sq)
                
                if distance > planet.radius + obj.radius:  # Avoid division by zero
                    # F = G * m1 * m2 / r^2, but we assume obj mass = 1
                    force = self.G * planet.mass / distance_sq
                    ax += force * dx / distance
                    ay += force * dy / distance
            
            # Apply acceleration to velocity
            obj.vx += ax * dt
            obj.vy += ay * dt
    
    def check_collisions(self):
        """Check for collisions between objects"""
        # Spaceship vs planets
        if self.spaceship and self.spaceship.alive and self.spaceship.invulnerable_time <= 0:
            for planet in self.planets:
                if not planet.alive:
                    continue
                    
                dist = math.sqrt((self.spaceship.x - planet.x)**2 + (self.spaceship.y - planet.y)**2)
                if dist < self.spaceship.radius + planet.radius:
                    if not self.spaceship.shield:
                        self.spaceship_hit()
                    break
        
        # Bullets vs planets
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
                
            for planet in self.planets[:]:
                if not planet.alive:
                    continue
                    
                dist = math.sqrt((bullet.x - planet.x)**2 + (bullet.y - planet.y)**2)
                if dist < bullet.radius + planet.radius:
                    self.planet_destroyed(planet)
                    bullet.alive = False
                    break
    
    def spaceship_hit(self):
        """Handle spaceship being hit"""
        self.lives -= 1
        self.spaceship.invulnerable_time = 2.0  # 2 seconds of invulnerability
        
        if self.lives <= 0:
            self.game_over = True
        else:
            # Respawn spaceship at center
            self.spaceship.x = self.canvas_width // 2
            self.spaceship.y = self.canvas_height // 2
            self.spaceship.vx = self.spaceship.vy = 0
    
    def planet_destroyed(self, planet):
        """Handle planet destruction"""
        self.score += planet.points
        
        # Special planet effects
        if planet.planet_type == "fuel":
            self.spaceship.fuel = min(self.spaceship.max_fuel, self.spaceship.fuel + 50)
        elif planet.planet_type == "explosive":
            # Chain reaction - damage nearby planets
            for other_planet in self.planets:
                if other_planet != planet and other_planet.alive:
                    dist = math.sqrt((planet.x - other_planet.x)**2 + (planet.y - other_planet.y)**2)
                    if dist < 100:  # Explosion radius
                        self.planet_destroyed(other_planet)
        
        planet.alive = False
        
        # Check if level complete
        if all(not p.alive for p in self.planets):
            self.level_complete = True
    
    def update_game(self, dt):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Handle continuous key presses
        if 'Left' in self.keys_pressed:
            self.spaceship.rotate(-1, dt)
        if 'Right' in self.keys_pressed:
            self.spaceship.rotate(1, dt)
        if 'Up' in self.keys_pressed:
            self.spaceship.apply_thrust(dt)
        
        # Apply gravity
        self.apply_gravity(dt)
        
        # Update all objects
        if self.spaceship:
            self.spaceship.update(dt)
            
        for planet in self.planets:
            if planet.alive:
                planet.update(dt)
        
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not bullet.alive:
                self.bullets.remove(bullet)
        
        # Keep objects within bounds
        self.wrap_around_screen()
        
        # Check collisions
        self.check_collisions()
        
        # Remove dead planets
        self.planets = [p for p in self.planets if p.alive]
        
        # Check level completion
        if self.level_complete:
            self.next_level()
    
    def wrap_around_screen(self):
        """Wrap objects around screen edges"""
        for obj in [self.spaceship] + self.bullets + self.planets:
            if not obj or not obj.alive:
                continue
                
            if obj.x < 0:
                obj.x = self.canvas_width
            elif obj.x > self.canvas_width:
                obj.x = 0
                
            if obj.y < 0:
                obj.y = self.canvas_height
            elif obj.y > self.canvas_height:
                obj.y = 0
    
    def draw_game(self):
        """Draw the game"""
        self.canvas.delete("all")
        
        # Draw background grid
        for i in range(0, self.canvas_width + 1, 50):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill="#222222", width=1)
        for i in range(0, self.canvas_height + 1, 50):
            self.canvas.create_line(0, i, self.canvas_width, i, fill="#222222", width=1)
        
        # Draw objects
        for planet in self.planets:
            if planet.alive:
                planet.draw(self.canvas)
        
        for bullet in self.bullets:
            if bullet.alive:
                bullet.draw(self.canvas)
        
        if self.spaceship and self.spaceship.alive:
            self.spaceship.draw(self.canvas)
        
        # Draw UI elements
        if self.paused:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                  text="PAUSED", fill="yellow", font=("Arial", 24, "bold"))
        
        if self.game_over:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                  text="GAME OVER", fill="red", font=("Arial", 24, "bold"))
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40,
                                  text=f"Final Score: {self.score}", fill="yellow", font=("Arial", 14))
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 70,
                                  text="Press R to restart game", fill="white", font=("Arial", 12))
        
        # Update info labels
        self.level_label.config(text=f"Level: {self.level}")
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.lives}")
        
        if self.spaceship:
            fuel_percent = int((self.spaceship.fuel / self.spaceship.max_fuel) * 100)
            self.fuel_label.config(text=f"Fuel: {fuel_percent}%")
    
    def game_loop(self):
        """Main game loop"""
        current_time = time.time()
        if hasattr(self, 'last_time'):
            dt = current_time - self.last_time
        else:
            dt = 0.016  # ~60 FPS
        
        self.last_time = current_time
        
        self.update_game(dt)
        self.draw_game()
        
        # Schedule next frame
        self.root.after(16, self.game_loop)  # ~60 FPS
    
    def run(self):
        """Start the game"""
        self.game_loop()
        self.root.mainloop()

if __name__ == "__main__":
    game = GravitationalDestroyer()
    game.run()
