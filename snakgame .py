import tkinter as tk
import random
import sys

# -------------------- CONFIG --------------------
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
SPEED = 80  # Lower is faster

# COLORS
BG_COLOR = "#050510"       # Deep Space Black
SNAKE_COLOR = "#00FF00"    # Neon Green
SNAKE_HEAD = "#CCFF00"     # Brighter Green
FOOD_COLOR = "#FF0044"     # Neon Red/Pink
SCORE_COLOR = "#00FFFF"    # Neon Cyan
GAME_OVER_COLOR = "#FF0000"

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NEON SNAKE 2025")
        self.resizable(False, False)
        
        # Center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (WIDTH // 2)
        y = (screen_height // 2) - (HEIGHT // 2)
        self.geometry(f"{WIDTH}x{HEIGHT}+{int(x)}+{int(y)}")
        
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        self.canvas = tk.Canvas(self, bg=BG_COLOR, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()
        
        # Score Board (Floating)
        self.score = 0
        self.score_id = self.canvas.create_text(
            WIDTH/2, 40, text=f"SCORE: {self.score}", 
            fill=SCORE_COLOR, font=("Consolas", 24, "bold"),
            state="hidden" # Hidden initially until game starts logic runs
        )
        
        # Bindings
        self.bind("<Left>", lambda e: self.change_dir("Left"))
        self.bind("<Right>", lambda e: self.change_dir("Right"))
        self.bind("<Up>", lambda e: self.change_dir("Up"))
        self.bind("<Down>", lambda e: self.change_dir("Down"))
        
        # WASD Support
        self.bind("w", lambda e: self.change_dir("Up"))
        self.bind("a", lambda e: self.change_dir("Left"))
        self.bind("s", lambda e: self.change_dir("Down"))
        self.bind("d", lambda e: self.change_dir("Right"))
        
        self.bind("<space>", lambda e: self.restart_game())

        # Restart Button (Hidden initially)
        btn_style = {"bg": "#FF0044", "fg": "white", "font": ("Consolas", 12, "bold"), "relief": "flat", "activebackground": "#ff3366"}
        self.restart_btn = tk.Button(self, text="RESTART GAME", command=self.restart_game, **btn_style)
        
    def new_game(self):
        self.canvas.delete("all")
        self.restart_btn.place_forget() # Hide button
        
        # Background: Cyber Grid + Starfield
        self.draw_background_effects()
        
        self.snake = [(100, 100), (80, 100), (60, 100)] 
        self.direction = "Right"
        self.next_direction = "Right"
        self.food_pos = self.spawn_food()
        self.score = 0
        self.game_over_flag = False
        
        self.draw_snake()
        self.draw_food()
        
        # Floating Score (Neon Style)
        self.score_id = self.canvas.create_text(
            WIDTH/2, 40, text=f"SCORE: 0", 
            fill=SCORE_COLOR, font=("Consolas", 24, "bold"),
            # Add a shadow/glow text behind it
        )

        self.update_game()
        
    def draw_background_effects(self):
        # Draw faint grid
        for i in range(0, WIDTH, GRID_SIZE):
            self.canvas.create_line(i, 0, i, HEIGHT, fill="#0f0f1f", width=1)
        for i in range(0, HEIGHT, GRID_SIZE):
            self.canvas.create_line(0, i, WIDTH, i, fill="#0f0f1f", width=1)
            
        # Draw "Stars" / Particles
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            color = random.choice(["#333344", "#555566", "#1a1a2e"])
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")

    def spawn_food(self):
        while True:
            x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
            y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food_pos
        
        # Pulsing Glow Effect (3 layers)
        for i in range(3):
            offset = (i+1) * 2
            alpha_color = "#330011" if i == 2 else "#660022"
            self.canvas.create_oval(
                x - offset, y - offset, x + GRID_SIZE + offset, y + GRID_SIZE + offset,
                outline=alpha_color, width=1, tags="food"
            )
            
        # Core
        self.canvas.create_oval(
            x + 2, y + 2, x + GRID_SIZE - 2, y + GRID_SIZE - 2,
            fill=FOOD_COLOR, outline="#FFFFFF", width=1, tags="food"
        )

    def draw_snake(self):
        self.canvas.delete("snake")
        
        for i, (x, y) in enumerate(self.snake):
            # Gradient Effect: Head is bright, tail gets darker
            if i == 0:
                color = SNAKE_HEAD
                outline = "#ffffff"
            else:
                # Alternating simplified cyber pattern
                color = SNAKE_COLOR if i % 2 == 0 else "#00cc00"
                outline = ""
                
            self.canvas.create_rectangle(
                x, y, x + GRID_SIZE, y + GRID_SIZE,
                fill=color, outline=outline, width=1, tags="snake"
            )
            
            # Decoration for Head
            if i == 0:
                # Cyber Eyes
                self.canvas.create_rectangle(x+4, y+4, x+8, y+8, fill="black", tags="snake")
                self.canvas.create_rectangle(x+12, y+4, x+16, y+8, fill="black", tags="snake")

    def change_dir(self, new_dir):
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_dir != opposites.get(self.direction):
            self.next_direction = new_dir

    def update_game(self):
        if self.game_over_flag:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Left":
            head_x -= GRID_SIZE
        elif self.direction == "Right":
            head_x += GRID_SIZE
        elif self.direction == "Up":
            head_y -= GRID_SIZE
        elif self.direction == "Down":
            head_y += GRID_SIZE
            
        new_head = (head_x, head_y)

        # Collision
        if (head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT or 
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food_pos:
            self.score += 10
            self.canvas.itemconfig(self.score_id, text=f"SCORE: {self.score}")
            self.food_pos = self.spawn_food()
            self.draw_food()
        else:
            self.snake.pop()

        self.draw_snake()
        self.after(SPEED, self.update_game)

    def game_over(self):
        self.game_over_flag = True
        
        # Semi-transparent overlay effect (simulated with stipple)
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#000000", stipple="gray50")
        
        self.canvas.create_text(
            WIDTH/2, HEIGHT/2 - 20, text="GAME OVER", 
            fill=GAME_OVER_COLOR, font=("Consolas", 60, "bold")
        )
        self.canvas.create_text(
            WIDTH/2, HEIGHT/2 + 40, text=f"FINAL SCORE: {self.score}", 
            fill=SCORE_COLOR, font=("Consolas", 30)
        )
        
        # Show Restart Button
        self.restart_btn.place(x=WIDTH/2 - 70, y=HEIGHT/2 + 80, width=140, height=40)

        
    def restart_game(self):
        if self.game_over_flag:
            self.new_game()

if __name__ == "__main__":
    app = SnakeGame()
    app.mainloop()
