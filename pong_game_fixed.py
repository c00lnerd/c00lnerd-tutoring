from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.score = 0
    
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        # Ball hits top of screen
        if pos[1] <= 0:
            self.y = 3
        
        # Ball hits bottom of screen
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        
        # Ball hits paddle
        if self.hit_paddle(pos) == True:
            self.y = -3
            self.score += 1
        
        # Ball hits left side
        if pos[0] <= 0:
            self.x = 3
        
        # Ball hits right side
        if pos[2] >= self.canvas_width:
            self.x = -3
    
    def reset(self):
        """Reset ball to starting position"""
        self.canvas.coords(self.id, 10, 10, 25, 25)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.hit_bottom = False
        self.score = 0

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.left_pressed = False
        self.right_pressed = False
        
        # Bind key press and release events
        self.canvas.bind_all('<KeyPress-Left>', self.left_down)
        self.canvas.bind_all('<KeyRelease-Left>', self.left_up)
        self.canvas.bind_all('<KeyPress-Right>', self.right_down)
        self.canvas.bind_all('<KeyRelease-Right>', self.right_up)
        self.canvas.bind_all('<KeyPress-space>', self.restart_game)
        
        # Store reference to ball for restart functionality
        self.ball = None
    
    def draw(self):
        # Update movement based on key states
        if self.left_pressed:
            self.x = -3
        elif self.right_pressed:
            self.x = 3
        else:
            self.x = 0
            
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        
        # Keep paddle on screen
        if pos[0] <= 0:
            self.canvas.move(self.id, -pos[0], 0)
        elif pos[2] >= self.canvas_width:
            self.canvas.move(self.id, self.canvas_width - pos[2], 0)
    
    def left_down(self, evt):
        self.left_pressed = True
    
    def left_up(self, evt):
        self.left_pressed = False
    
    def right_down(self, evt):
        self.right_pressed = True
    
    def right_up(self, evt):
        self.right_pressed = False
    
    def restart_game(self, evt):
        if self.ball and self.ball.hit_bottom:
            self.ball.reset()

# Create the main game window
tk = Tk()
tk.title("Pong Game - Arrow Keys: Move | Space: Restart")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

# Make sure the window can receive keyboard input
canvas.focus_set()
tk.update()

# Create paddle and ball
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

# Link paddle to ball for restart functionality
paddle.ball = ball

# Create score display
score_text = canvas.create_text(50, 20, text="Score: 0", fill="black", font=("Arial", 16))
game_over_text = None

# Game loop
while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
        
        # Update score display
        canvas.itemconfig(score_text, text=f"Score: {ball.score}")
        
        # Remove game over text if it exists
        if game_over_text:
            canvas.delete(game_over_text)
            game_over_text = None
    else:
        # Game over - show message
        if not game_over_text:
            game_over_text = canvas.create_text(250, 200, 
                text=f"GAME OVER!\nFinal Score: {ball.score}\nPress SPACE to restart", 
                fill="red", font=("Arial", 20), justify="center")
    
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
