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
    # Startup: 1 on Top, 2 on Bottom
    draw_num('1', x=2, y=2)      # Top (y approx 0-7)
    draw_num('2', x=2, y=10)     # Bottom (y approx 8-15)

def update(dt, inputs):
    """
    Called every frame.
    dt: Time delta in seconds.
    inputs: Dictionary of button states (e.g., {'UP': True, 'DOWN': False}).
    """
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
        draw_num('1', x=2, y=2)
        active = True
    elif inputs['2']:
        draw_num('2', x=2, y=10)
        active = True
        
    if not active:
        # If we want the startup numbers to persist until pressed, 
        # we need state. But user says "on start up display...".
        # Assuming pressing buttons overrides it.
        # To make startup persist until input, we need a "touched" flag.
        # For now, let's clear if no input, which implies startup vanishes on first frame?
        # Ideally, we only clear if keys *were* pressed or we want blank when idle.
        # User code previously cleared on release.
        # Let's keep existing "Default Clear" behavior but we need to check if we just started.
        # Actually user ran "pause()" before so it stayed.
        # Here we run a loop.
        # Let's add a dirty check or just let it vanish on first keypress?
        # User request: "on start up display...".
        # If I clear_grid() here immediately when no buttons are pressed, it disappears instantly.
        # I should output the grid once in init, and only clear if inputs change?
        # Let's clear ONLY if buttons are NOT pressed but were? 
        # Simplest: If ANY button pressed -> Draw. Else -> Clear. 
        # This wipes the startup numbers instantly. 
        # I will add a 'started' flag to keep numbers until first press.
        pass
    
    # Logic to keep startup display until first press:
    is_any_pressed = any(inputs.values())
    if is_any_pressed:
        if not hasattr(update, "has_pressed"):
            update.has_pressed = True
    
    if is_any_pressed:
       pass # Drawing handled above
    elif getattr(update, "has_pressed", False):
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
    # Middle ish (Top Screen for consistency with UP/LEFT mapping?)
    # Arrow pointing Left
    for i in range(5): set_pixel(5-i, 4, 1)
    set_pixel(2, 3, 1); set_pixel(2, 5, 1); set_pixel(1, 4, 1)

def draw_arrow_right():
    clear_grid()
    # Right Arrow
    for i in range(5): set_pixel(2+i, 4, 1)
    set_pixel(5, 3, 1); set_pixel(5, 5, 1); set_pixel(6, 4, 1)

def draw_num(n, x=2, y=2):
    # clear_grid() # Don't clear here to allow multiple numbers? 
    # User logic implies one at a time usually, but startup has two.
    # Manual clear in update handles interaction.
    draw_bitmap(x, y, NUMBERS[n])
