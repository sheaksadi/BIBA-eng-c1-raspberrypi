import snake
import tetris
import frogger
import space_invaders
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
STATE_FROGGER = 3
STATE_INVADERS = 4

current_state = STATE_MENU

def init():
    """Called once at startup."""
    print("Main System Initialized")
    
def update(dt, inputs):
    global current_state

    # Global Reset to Menu (Button 1+2 held? Or maybe just rely on logic)
    # For now, let's keep it simple.
    
    if current_state == STATE_MENU:
        update_menu(dt, inputs)
    elif current_state == STATE_SNAKE:
        snake.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_TETRIS:
        tetris.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_FROGGER:
        frogger.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_INVADERS:
        space_invaders.update(dt, inputs)
        check_exit(inputs)

def check_exit(inputs):
    global current_state
    if inputs['LEFT'] and inputs['RIGHT']:
         current_state = STATE_MENU
         audio.stop_music()
         win_pause(0.5)

def draw():
    clear_grid()
    
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_SNAKE:
        snake.draw(grid)
    elif current_state == STATE_TETRIS:
        tetris.draw(grid)
    elif current_state == STATE_FROGGER:
        frogger.draw(grid)
    elif current_state == STATE_INVADERS:
        space_invaders.draw(grid)

# --- Menu Logic ---

menu_selection = 0 
# 0=Snake, 1=Tetris, 2=Frogger, 3=Invaders

def update_menu(dt, inputs):
    global current_state, menu_selection
    
    # Selection (Up/Down cycles through 4 items)
    old_sel = menu_selection
    if inputs['UP'] or inputs['LEFT']:
        menu_selection = (menu_selection - 1) % 4
    elif inputs['DOWN'] or inputs['RIGHT']:
        menu_selection = (menu_selection + 1) % 4
        
    if old_sel != menu_selection:
        audio.sfx_move()
        # Initial delay to prevent super fast scrolling? 
        # Inputs are typically polled fast. Assuming run.py sleep(0.016) is fine.
        win_pause(0.15) # Small debounce
        
    # Confirm
    if inputs['1'] or inputs['2']:
        audio.sfx_select()
        if menu_selection == 0:
            print("Starting Snake")
            snake.init()
            current_state = STATE_SNAKE
        elif menu_selection == 1:
            print("Starting Tetris")
            tetris.init()
            current_state = STATE_TETRIS
        elif menu_selection == 2:
            print("Starting Frogger")
            frogger.init()
            current_state = STATE_FROGGER
        elif menu_selection == 3:
            print("Starting Space Invaders")
            space_invaders.init()
            current_state = STATE_INVADERS
        win_pause(0.5)

def draw_menu():
    # Draw Menu: 4 Icons if they fit?
    # Screen is 8x16.
    # Let's show 2 items at a time? Or just one big letter?
    # Simpler: 4 Small Icons vertically.
    # Snake: S-like shape (y=1)
    # Tetris: T-like shape (y=5)
    # Frogger: F-like shape (y=9)
    # Invaders: I/Alien-like shape (y=13)
    
    # Selection Box
    sel_y = 1 + (menu_selection * 4)
    # Set pixel to left of selected item
    set_pixel(0, sel_y+1, 1)
    
    # Snake Icon (S)
    set_pixel(2, 1, 1); set_pixel(3, 1, 1); set_pixel(4, 1, 1)
    set_pixel(2, 2, 1)
    set_pixel(2, 3, 1); set_pixel(3, 3, 1); set_pixel(4, 3, 1)
    
    # Tetris Icon (T)
    set_pixel(2, 5, 1); set_pixel(3, 5, 1); set_pixel(4, 5, 1)
    set_pixel(3, 6, 1)
    set_pixel(3, 7, 1)

    # Frogger (F)
    set_pixel(2, 9, 1); set_pixel(3, 9, 1); set_pixel(4, 9, 1)
    set_pixel(2, 10, 1); set_pixel(3, 10, 1)
    set_pixel(2, 11, 1)
    
    # Invaders (Space Ship / Alien)
    # Mini Alien
    set_pixel(2, 14, 1); set_pixel(4, 14, 1)
    set_pixel(3, 13, 1); 
    set_pixel(2, 15, 1); set_pixel(3, 15, 1); set_pixel(4, 15, 1)

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

