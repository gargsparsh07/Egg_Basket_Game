from itertools import cycle
from random import randint, choice
from tkinter import Canvas, Tk, messagebox, font

# Canvas dimensions
WIDTH, HEIGHT = 800, 400

# Initialize window
root = Tk()
root.title("Egg Catcher")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background="deep sky blue")
canvas.create_rectangle(-5, HEIGHT-100, WIDTH+5, HEIGHT+5, fill="sea green", width=0)
canvas.create_oval(-80, -80, 120, 120, fill='orange', width=0)
canvas.pack()

# Game variables
COLORS = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
EGG_SIZE = (45, 55)
EGG_SCORE = 10
EGG_SPEED = 500
EGG_INTERVAL = 4000
DIFFICULTY = 0.95
CATCHER_SPEED = 20  # Default movement speed

# Special golden egg
GOLDEN_EGG_PROBABILITY = 0.2  # 20% chance
GOLDEN_EGG_SCORE = 50
golden_egg_color = "gold"

# Catcher properties
CATCHER_COLOR = "blue"
CATCHER_SIZE = (100, 100)
CATCHER_X = WIDTH / 2 - CATCHER_SIZE[0] / 2
CATCHER_Y = HEIGHT - CATCHER_SIZE[1] - 20

# Create catcher
catcher = canvas.create_arc(
    CATCHER_X, CATCHER_Y, CATCHER_X + CATCHER_SIZE[0], CATCHER_Y + CATCHER_SIZE[1],
    start=200, extent=140, style="arc", outline=CATCHER_COLOR, width=3
)

# Game font
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

# Score and lives
score = 0
score_text = canvas.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text=f"Score: {score}")

lives = 3
lives_text = canvas.create_text(WIDTH-10, 10, anchor="ne", font=game_font, fill="darkblue", text=f"Lives: {lives}")

# Egg list
eggs = []

def create_egg():
    """Creates an egg at a random position, with a small chance to be golden."""
    x = randint(20, WIDTH - 60)
    y = 40
    is_golden = choice([True, False]) if randint(1, 10) <= GOLDEN_EGG_PROBABILITY * 10 else False
    color = golden_egg_color if is_golden else next(COLORS)
    new_egg = canvas.create_oval(x, y, x + EGG_SIZE[0], y + EGG_SIZE[1], fill=color, width=0)
    eggs.append((new_egg, is_golden))  # Store if it's golden
    root.after(EGG_INTERVAL, create_egg)

def move_eggs():
    """Moves all eggs downward and checks if they hit the ground."""
    for egg, is_golden in eggs:
        (x1, y1, x2, y2) = canvas.coords(egg)
        canvas.move(egg, 0, 10)
        if y2 > HEIGHT:
            egg_dropped(egg)
    root.after(EGG_SPEED, move_eggs)

def egg_dropped(egg):
    """Handles dropped eggs."""
    global eggs
    eggs = [(e, g) for e, g in eggs if e != egg]  # Remove from list
    canvas.delete(egg)
    lose_life()
    if lives == 0:
        messagebox.showinfo("Game Over!", f"Final Score: {score}")
        root.destroy()

def lose_life():
    """Reduces lives when an egg is missed."""
    global lives
    lives -= 1
    canvas.itemconfigure(lives_text, text=f"Lives: {lives}")

def check_catch():
    """Checks if an egg is caught by the catcher."""
    global eggs
    (catcher_x1, catcher_y1, catcher_x2, catcher_y2) = canvas.coords(catcher)
    new_eggs = []
    
    for egg, is_golden in eggs:
        (egg_x1, egg_y1, egg_x2, egg_y2) = canvas.coords(egg)
        if catcher_x1 < egg_x1 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            canvas.delete(egg)
            increase_score(GOLDEN_EGG_SCORE if is_golden else EGG_SCORE)
            if is_golden:
                activate_speed_boost()
        else:
            new_eggs.append((egg, is_golden))
    
    eggs = new_eggs
    root.after(100, check_catch)

def increase_score(points):
    """Increases the score and speeds up the game."""
    global score, EGG_SPEED, EGG_INTERVAL
    score += points
    EGG_SPEED = int(EGG_SPEED * DIFFICULTY)
    EGG_INTERVAL = int(EGG_INTERVAL * DIFFICULTY)
    canvas.itemconfigure(score_text, text=f"Score: {score}")

def activate_speed_boost():
    """Temporarily increases the catcher movement speed when catching a golden egg."""
    global CATCHER_SPEED
    original_speed = CATCHER_SPEED
    CATCHER_SPEED = 30  # Increase speed
    root.after(5000, lambda: reset_speed(original_speed))  # Reset after 5 seconds

def reset_speed(original_speed):
    """Resets catcher speed after power-up expires."""
    global CATCHER_SPEED
    CATCHER_SPEED = original_speed

def move_left(event):
    """Moves the catcher left."""
    (x1, _, x2, _) = canvas.coords(catcher)
    if x1 > 0:
        canvas.move(catcher, -CATCHER_SPEED, 0)

def move_right(event):
    """Moves the catcher right."""
    (x1, _, x2, _) = canvas.coords(catcher)
    if x2 < WIDTH:
        canvas.move(catcher, CATCHER_SPEED, 0)

# Bind keys
canvas.bind("<Left>", move_left)
canvas.bind("<Right>", move_right)
canvas.focus_set()

# Start game
root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()
