import audio

WIDTH = 8
HEIGHT = 16

# Game State
player_pos = [4, 15] # Start at bottom center
lives = 3
score = 0
game_over = False
timer = 0
level_timer = 0

# Rows (Type, Speed, Pattern)
# Types: 0=Safe, 1=Water(Log), 2=Road(Car), 3=Goal
# Speed: +/- cells per second
ROWS = [
    {'type': 3, 'speed': 0, 'pattern': []},      # 0: Goal
    {'type': 1, 'speed': 2, 'pattern': [1,0,0,1]}, # 1: River
    {'type': 1, 'speed': -3, 'pattern': [0,1,1,0]}, # 2: River
    {'type': 1, 'speed': 4, 'pattern': [1,0,0,0]}, # 3: River
    {'type': 0, 'speed': 0, 'pattern': []},      # 4: Safe Bank
    {'type': 2, 'speed': -2, 'pattern': [1,0,0,1]}, # 5: Road
    {'type': 2, 'speed': 3, 'pattern': [0,0,1,0]}, # 6: Road
    {'type': 2, 'speed': -4, 'pattern': [1,0,1,0]}, # 7: Road
    {'type': 2, 'speed': 4, 'pattern': [0,1,0,0]}, # 8: Road
    {'type': 0, 'speed': 0, 'pattern': []},      # 9: Safe
    {'type': 0, 'speed': 0, 'pattern': []},      # 10: Safe
    {'type': 0, 'speed': 0, 'pattern': []},      # 11: Safe
    {'type': 0, 'speed': 0, 'pattern': []},      # 12: Safe
    {'type': 0, 'speed': 0, 'pattern': []},      # 13: Safe
    {'type': 0, 'speed': 0, 'pattern': []},      # 14: Safe
    {'type': 0, 'speed': 0, 'pattern': []}       # 15: Start
]

# Row offsets for scrolling
row_offsets = [0.0] * HEIGHT

def init():
    global player_pos, lives, score, game_over, row_offsets
    player_pos = [4, 15]
    lives = 3
    score = 0
    game_over = False
    row_offsets = [0.0] * HEIGHT
    audio.play_music('frogger')

def reset_pos():
    global player_pos
    player_pos = [4, 15]

def update(dt, inputs):
    global timer, game_over, score, lives
    
    if game_over:
        if inputs['1'] or inputs['2']:
            init()
        return
    
    # Input (Detect Press)
    # Using simple delay or edge detection?
    # Simple repeat delay for movement
    if not hasattr(update, 'last_move'): update.last_move = 0
    update.last_move += dt
    
    dx, dy = 0, 0
    if update.last_move > 0.15:
        if inputs['UP']: dy = -1
        elif inputs['DOWN']: dy = 1
        elif inputs['LEFT']: dx = -1
        elif inputs['RIGHT']: dx = 1
        
        if dx != 0 or dy != 0:
            audio.sfx_jump()
            update.last_move = 0
            # Move
            player_pos[0] = max(0, min(WIDTH-1, player_pos[0] + dx))
            player_pos[1] = max(0, min(HEIGHT-1, player_pos[1] + dy))
            
            # Check Win (Goal)
            if player_pos[1] == 0:
                score += 100
                audio.sfx_select() # Reuse success sound
                reset_pos()

    # Update Rows
    for i, row in enumerate(ROWS):
        if row['speed'] != 0:
            row_offsets[i] += row['speed'] * dt
            # Wrap offset
            # Pattern length is usually 4 or 8. Let's assume 8 for smoothness?
            # Or simplified: Pattern repeats every len(pattern)
            # If offset grows, we just use modulo when drawing/colliding.
            
    # Collision Logic
    py_int = int(player_pos[1])
    px_int = int(player_pos[0])
    
    # Check bounds
    if py_int < 0 or py_int >= HEIGHT: return # Should not happen
    
    row = ROWS[py_int]
    
    if row['type'] == 1: # Water
        # Must be on log (1). If 0 -> Drown
        if not is_safe(px_int, py_int):
            die()
    elif row['type'] == 2: # Road
        # Must NOT be on car (1). If 1 -> Squash
        if is_occupied(px_int, py_int):
            die()

def is_occupied(x, y):
    row = ROWS[y]
    if not row['pattern']: return False
    
    # Calculate effective index in pattern
    # Pattern moves LEFT if speed > 0? Or RIGHT?
    # Usually speed > 0 means objects move RIGHT.
    # So effective_x = x - offset
    
    pat = row['pattern']
    offset = row_offsets[y]
    L = len(pat)
    
    # Map x to pattern space
    pat_idx = int((x - offset) % L)
    
    return pat[pat_idx] == 1

def is_safe(x, y):
    # For water: safe if occupied (Log)
    return is_occupied(x, y)

def die():
    global lives, game_over
    lives -= 1
    audio.sfx_crash()
    if lives <= 0:
        game_over = True
        audio.stop_music()
    else:
        reset_pos()

def draw(grid):
    # Draw Background/Obstacles
    for y in range(HEIGHT):
        row = ROWS[y]
        pat = row['pattern']
        if pat:
            offset = row_offsets[y]
            L = len(pat)
            for x in range(WIDTH):
                pat_idx = int((x - offset) % L)
                val = pat[pat_idx]
                if val:
                    grid[y][x] = 1 # Car or Log
            
            # Invert water? No, LED matrix is black. 
            # Logs are lit (1). Water is dark (0).
            # So if on Log (1), safe.
            # Cars are lit (1). If hit, die.
    
    # Draw Player (Flash if collision? Just static for now)
    px, py = player_pos
    if not game_over:
        grid[py][px] = 1 # Draw Player
        
        # Blink player if on safe log to distinguish?
        # Or make player always ON, and logs blinking?
        # Hard on 1-bit display.
        # Let's trust logic.
        pass
        
    if game_over:
        # Draw X
        for i in range(8): grid[i][i] = 1; grid[i][7-i] = 1
