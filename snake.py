import tkinter as tk
import random

# Game window layout configurations
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"      # Green
FOOD_COLOR = "#FF0000"       # Red
BACKGROUND_COLOR = "#000000"  # Black

# Difficulty levels configuration map (Speed in milliseconds)
DIFFICULTY_SPEEDS = {
    "Easy": 250,
    "Medium": 130,
    "Hard": 70
}

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global is_paused, game_running, current_difficulty
    
    if is_paused or not game_running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if snake eats food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        
        # Check and update real-time high score for current level
        if score > high_scores[current_difficulty]:
            high_scores[current_difficulty] = score
            update_high_score_display()
            
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        current_speed = DIFFICULTY_SPEEDS[current_difficulty]
        window.after(current_speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if is_paused or not game_running:
        return
        
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def pause_game():
    global is_paused
    if game_running:
        is_paused = True

def resume_game():
    global is_paused
    if is_paused and game_running:
        is_paused = False
        next_turn(snake, food)

def restart_game():
    global score, direction, is_paused, game_running, snake, food
    
    score = 0
    direction = 'down'
    is_paused = False
    game_running = True
    
    label.config(text="Score: {}".format(score))
    update_high_score_display()
    canvas.delete(tk.ALL)
    
    snake = Snake()
    food = Food()
    next_turn(snake, food)

def change_difficulty(selected_level):
    global current_difficulty
    current_difficulty = selected_level
    update_high_score_display()
    restart_game()

def update_high_score_display():
    high_score_label.config(text=f"High Score ({current_difficulty}): {high_scores[current_difficulty]}")

def game_over():
    global game_running
    game_running = False
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('sans-serif', 40), text="GAME OVER", fill="red", tag="gameover")

# Window setup
window = tk.Tk()
window.title("Snake Game with Unified Controls")
window.resizable(False, False)

# Track state values
score = 0
direction = 'down'
is_paused = False
game_running = True
current_difficulty = "Easy"

# Dictionary holding tracking entries for highest historical attempts
high_scores = {"Easy": 0, "Medium": 0, "Hard": 0}

# Unified Top Frame: Holds all action control items side-by-side
top_control_panel = tk.Frame(window)
top_control_panel.pack(pady=10, fill=tk.X)

# --- Difficulty Controls Group ---
difficulty_label = tk.Label(top_control_panel, text="Difficulty: ", font=('sans-serif', 11))
difficulty_label.pack(side=tk.LEFT, padx=(10, 2))

for level in ["Easy", "Medium", "Hard"]:
    btn = tk.Button(top_control_panel, text=level, font=('sans-serif', 9), 
                    command=lambda l=level: change_difficulty(l))
    btn.pack(side=tk.LEFT, padx=2)

# --- Game State Action Controls Group (Moved to the Top Row) ---
restart_btn = tk.Button(top_control_panel, text="Restart", font=('sans-serif', 9), width=8, command=restart_game)
restart_btn.pack(side=tk.RIGHT, padx=(2, 10))

resume_btn = tk.Button(top_control_panel, text="Resume", font=('sans-serif', 9), width=8, command=resume_game)
resume_btn.pack(side=tk.RIGHT, padx=2)

pause_btn = tk.Button(top_control_panel, text="Pause", font=('sans-serif', 9), width=8, command=pause_game)
pause_btn.pack(side=tk.RIGHT, padx=2)

# Sub-Header Panel: Scoreboard indicators
stats_panel = tk.Frame(window)
stats_panel.pack(fill=tk.X, padx=10)

label = tk.Label(stats_panel, text="Score: 0", font=('sans-serif', 16))
label.pack(side=tk.LEFT)

high_score_label = tk.Label(stats_panel, text="High Score (Easy): 0", font=('sans-serif', 12), fg="blue")
high_score_label.pack(side=tk.RIGHT)

# Drawing Canvas Container setup
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack(pady=(5, 15))

window.update()

# Center window on screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Keyboard directional bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start initial state configurations
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
