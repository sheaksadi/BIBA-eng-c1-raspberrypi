import snake
import tetris
import block_breaker
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
STATE_BREAKOUT = 3
STATE_INVADERS = 4

current_state = STATE_MENU

def init():
    """Called once at startup."""
    print("Main System Initialized")
    
def update(dt, inputs):
    global current_state

    if current_state == STATE_MENU:
        update_menu(dt, inputs)
    elif current_state == STATE_SNAKE:
        snake.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_TETRIS:
        tetris.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_BREAKOUT:
        block_breaker.update(dt, inputs)
        check_exit(inputs)
    elif current_state == STATE_INVADERS:
        space_invaders.update(dt, inputs)
        check_exit(inputs)

def check_exit(inputs):
    global current_state
    # Button 2 = Back to Menu
    if inputs['2']:
        current_state = STATE_MENU
        audio.stop_music()
        win_pause(0.3)

def draw():
    clear_grid()
    
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_SNAKE:
        snake.draw(grid)
    elif current_state == STATE_TETRIS:
        tetris.draw(grid)
    elif current_state == STATE_BREAKOUT:
        block_breaker.draw(grid)
    elif current_state == STATE_INVADERS:
        space_invaders.draw(grid)

# --- Menu Logic ---

menu_selection = 0 
# 0=Snake, 1=Tetris, 2=Breakout, 3=Invaders

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
        win_pause(0.15)
        
    # Button 1 = Confirm/Enter
    if inputs['1']:
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
            print("Starting Block Breaker")
            block_breaker.init()
            current_state = STATE_BREAKOUT
        elif menu_selection == 3:
            print("Starting Space Invaders")
            space_invaders.init()
            current_state = STATE_INVADERS
        win_pause(0.5)

def draw_menu():
    # 4 Icons vertically: S, T, B, I
    # Selection indicator on left
    
    sel_y = 1 + (menu_selection * 4)
    set_pixel(0, sel_y+1, 1)
    
    # Snake Icon (S)
    set_pixel(2, 1, 1); set_pixel(3, 1, 1); set_pixel(4, 1, 1)
    set_pixel(2, 2, 1)
    set_pixel(2, 3, 1); set_pixel(3, 3, 1); set_pixel(4, 3, 1)
    
    # Tetris Icon (T)
    set_pixel(2, 5, 1); set_pixel(3, 5, 1); set_pixel(4, 5, 1)
    set_pixel(3, 6, 1)
    set_pixel(3, 7, 1)

    # Block Breaker (B)
    set_pixel(2, 9, 1); set_pixel(3, 9, 1)
    set_pixel(2, 10, 1); set_pixel(4, 10, 1)
    set_pixel(2, 11, 1); set_pixel(3, 11, 1)
    
    # Invaders (Alien)
    set_pixel(2, 14, 1); set_pixel(4, 14, 1)
    set_pixel(3, 13, 1)
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


