import random
import audio

WIDTH = 8
HEIGHT = 16
SPEED = 0.3 # Slower speed (was 0.15)

snake = []
dir = (0, 0)
food = (0, 0)
game_over = False
timer = 0
score = 0

def init():
    global snake, dir, food, game_over, timer, score
    snake = [(4, 10), (4, 11), (4, 12)]
    # ... rest same ...
    dir = (0, -1)
    game_over = False
    timer = 0
    score = 0
    spawn_food()
    audio.play_music('snake')

def spawn_food():
    global food
    while True:
        food = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
        if food not in snake:
            break

def update(dt, inputs):
    global timer, dir, game_over
    
    if game_over:
        if inputs['1'] or inputs['2']:
            init() # Restart
        return

    # Buffer input to prevent 180 turns
    if inputs['UP'] and dir != (0, 1): dir = (0, -1)
    elif inputs['DOWN'] and dir != (0, -1): dir = (0, 1)
    elif inputs['LEFT'] and dir != (1, 0): dir = (-1, 0)
    elif inputs['RIGHT'] and dir != (-1, 0): dir = (1, 0)

    timer += dt
    if timer >= SPEED:
        timer = 0
        step()

def step():
    global game_over, snake, score
    head = snake[0]
    # Move and Wrap around screen
    new_x = (head[0] + dir[0]) % WIDTH
    new_y = (head[1] + dir[1]) % HEIGHT
    new_head = (new_x, new_y)

    # Wall Collision removed (wrapping implemented)
    
    # Self Collision
    if new_head in snake:
        game_over = True
        audio.stop_music()
        audio.sfx_crash()
        return

    snake.insert(0, new_head)
    
    if new_head == food:
        score += 1
        audio.sfx_eat()
        spawn_food()
        # Speed up slightly every 5 points
        global SPEED
        if score % 5 == 0 and SPEED > 0.05:
            # SPEED -= 0.01 # Optional difficulty increase
            pass
    else:
        snake.pop()

def draw(grid):
    if game_over:
        # Draw "X" or something to show game over
        # Simple X pattern
        for i in range(8):
            grid[i][i] = 1
            grid[i][7-i] = 1
        return

    # Draw Snake
    for x, y in snake:
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            grid[y][x] = 1
            
    # Draw Food
    if 0 <= food[1] < HEIGHT and 0 <= food[0] < WIDTH:
        grid[food[1]][food[0]] = 1
