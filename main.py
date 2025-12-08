# main.py

# Dimensions
WIDTH = 8
HEIGHT = 16

# The 2D Array (Screen Buffer)
# 0 = Off, 1 = On
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Bitmaps (Optional, for demo)
NUMBERS = {
    '1': [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0]],
    '2': [[0,1,1,1,0],[0,0,0,0,1],[0,1,1,1,0],[0,1,0,0,0],[0,1,1,1,1]]
}

def init():
    """Called once at startup."""
    print("Game Initialized")
    clear_grid()

def update(dt, inputs):
    """
    Called every frame.
    dt: Time delta in seconds.
    inputs: Dictionary of button states (e.g., {'UP': True, 'DOWN': False}).
    """
    # clear_grid() # Optional: Clear every frame or persist? 
                 # User's previous code cleared on release. 
                 # Let's clear here if we want immediate feedback style.
    
    # Simple Demo Logic: Show Arrow/Number when held
    active = False
    
    if inputs['UP']:
        draw_arrow_up()
        active = True
    elif inputs['DOWN']:
        draw_arrow_down()
        active = True
    elif inputs['LEFT']:
        draw_arrow_left()
        active = True
    elif inputs['RIGHT']:
        draw_arrow_right()
        active = True
    elif inputs['1']:
        draw_num('1')
        active = True
    elif inputs['2']:
        draw_num('2')
        active = True
        
    if not active:
        clear_grid()

def draw():
    """
    Called every frame after update. 
    Use this to finalize the grid if needed.
    """
    pass

# --- Helper Functions ---

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

def draw_arrow_up():
    clear_grid()
    # Draw on Top Screen (y=0..7)
    for i in range(5): set_pixel(3, 6-i, 1)
    set_pixel(2, 3, 1); set_pixel(4, 3, 1); set_pixel(3, 2, 1)

def draw_arrow_down():
    clear_grid()
    # Draw on Bottom Screen (y=8..15)
    base_y = 8
    for i in range(5): set_pixel(3, base_y+1+i, 1)
    set_pixel(2, base_y+4, 1); set_pixel(4, base_y+4, 1); set_pixel(3, base_y+5, 1)

def draw_arrow_left():
    clear_grid()
    # Middle ish
    for i in range(5): set_pixel(5-i, 4, 1)
    set_pixel(2, 3, 1); set_pixel(2, 5, 1); set_pixel(1, 4, 1)

def draw_arrow_right():
    clear_grid()
    for i in range(5): set_pixel(2+i, 4, 1)
    set_pixel(5, 3, 1); set_pixel(5, 5, 1); set_pixel(6, 4, 1)

def draw_num(n):
    clear_grid()
    draw_bitmap(2, 2, NUMBERS[n])
