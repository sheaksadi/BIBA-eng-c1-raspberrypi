import snake
import tetris
import audio

# Dimensions
WIDTH = 8
HEIGHT = 16

# The 2D Array (Screen Buffer)
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# States
STATE_MENU = 0
STATE_SNAKE = 1
STATE_TETRIS = 2

current_state = STATE_MENU

def init():
    """Called once at startup."""
    print("Main System Initialized")
    # Initialize sub-games just in case
    # tetris.init() # We'll init when entering state
    # snake.init()
    
def update(dt, inputs):
    global current_state

    # Global Reset to Menu (Button 1+2 held? Or maybe just rely on logic)
    # For now, let's keep it simple.
    
    if current_state == STATE_MENU:
        update_menu(dt, inputs)
    elif current_state == STATE_SNAKE:
        snake.update(dt, inputs)
        # Exit condition? Maybe Button 1+2 Long Press?
        # For now, if Game Over, '1' or '2' restarts in snake.py.
        # Let's add a way to return to menu: 'LEFT' + 'RIGHT' together?
        if inputs['LEFT'] and inputs['RIGHT']:
             current_state = STATE_MENU
             win_pause(0.5)

    elif current_state == STATE_TETRIS:
        tetris.update(dt, inputs)
        if inputs['LEFT'] and inputs['RIGHT']:
             current_state = STATE_MENU
             win_pause(0.5)

def draw():
    clear_grid()
    
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_SNAKE:
        snake.draw(grid)
    elif current_state == STATE_TETRIS:
        tetris.draw(grid)

# --- Menu Logic ---

menu_selection = 0 # 0=Snake, 1=Tetris (Simple toggle)

def update_menu(dt, inputs):
    global current_state, menu_selection
    
    # Selection
    if inputs['UP'] or inputs['LEFT']:
        if menu_selection != 0:
            menu_selection = 0
            audio.sfx_move()
    elif inputs['DOWN'] or inputs['RIGHT']:
        if menu_selection != 1:
            menu_selection = 1
            audio.sfx_move()
        
    # Confirm
    if inputs['1'] or inputs['2']:
        audio.sfx_select()
        if menu_selection == 0:
            print("Starting Snake")
            snake.init()
            current_state = STATE_SNAKE
        else:
            print("Starting Tetris")
            tetris.init()
            current_state = STATE_TETRIS
        win_pause(0.5)

def draw_menu():
    # Draw 'S' for Snake on Top
    # Draw 'T' for Tetris on Bottom
    # Highlight selection with a dot or box?
    
    # S Bitmap
    s_bmp = [
        [0,1,1,1,0],
        [1,0,0,0,0],
        [0,1,1,0,0],
        [0,0,0,1,0],
        [1,1,1,0,0]
    ]
    draw_bitmap(2, 1, s_bmp)
    
    # T Bitmap
    t_bmp = [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ]
    draw_bitmap(2, 9, t_bmp)
    
    # Selection Indicator (Arrow or Dot)
    if menu_selection == 0:
        set_pixel(0, 3, 1) # Next to S
    else:
        set_pixel(0, 11, 1) # Next to T


# --- Common Helpers ---

def clear_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            grid[y][x] = 0

def set_pixel(x, y, val=1):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = val

def draw_bitmap(x, y, bitmap):
    h = len(bitmap)
    w = len(bitmap[0])
    for r in range(h):
        for c in range(w):
            if bitmap[r][c]:
                set_pixel(x + c, y + r, 1)

import time
def win_pause(sec):
    time.sleep(sec)

