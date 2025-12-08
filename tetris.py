import random

WIDTH = 8
HEIGHT = 16

# Shapes (Standard Tetrominoes)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]], # Z
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

board = []
current_piece = None
current_x = 0
current_y = 0
game_over = False
timer = 0
drop_speed = 0.5
fast_drop = False

def init():
    global board, game_over
    board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    game_over = False
    spawn_piece()

def spawn_piece():
    global current_piece, current_x, current_y, game_over
    shape = random.choice(SHAPES)
    current_piece = shape
    current_x = WIDTH // 2 - len(shape[0]) // 2
    current_y = 0
    
    if check_collision(current_piece, current_x, current_y):
        game_over = True

def check_collision(piece, off_x, off_y):
    for y, row in enumerate(piece):
        for x, val in enumerate(row):
            if val:
                bx = off_x + x
                by = off_y + y
                if bx < 0 or bx >= WIDTH or by >= HEIGHT:
                    return True
                if by >= 0 and board[by][bx]:
                    return True
    return False

def rotate_piece(piece):
    # Rotate 90 degrees clockwise
    return [list(row) for row in zip(*piece[::-1])]

def lock_piece():
    global board
    for y, row in enumerate(current_piece):
        for x, val in enumerate(row):
            if val:
                if 0 <= current_y + y < HEIGHT:
                    board[current_y + y][current_x + x] = 1
    clear_lines()
    spawn_piece()

def clear_lines():
    global board
    new_board = [row for row in board if any(v == 0 for v in row)]
    lines_cleared = HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * WIDTH)
    board = new_board

last_input_time = 0
INPUT_DELAY = 0.1

def update(dt, inputs):
    global timer, current_x, current_y, current_piece, last_input_time, fast_drop, game_over
    
    if game_over:
        if inputs['1'] or inputs['2']:
            init()
        return

    # Input Handling (with delay to prevent super fast movement)
    # Using simple delay for l/r/rotate
    last_input_time += dt
    if last_input_time > INPUT_DELAY:
        dx = 0
        if inputs['LEFT']: dx = -1
        elif inputs['RIGHT']: dx = 1
        
        if dx != 0:
            if not check_collision(current_piece, current_x + dx, current_y):
                current_x += dx
                last_input_time = 0
        
        if inputs['UP']: # Rotate
            rotated = rotate_piece(current_piece)
            if not check_collision(rotated, current_x, current_y):
                current_piece = rotated
                last_input_time = 0

    # Gravity
    fast_drop = inputs['DOWN']
    current_speed = 0.05 if fast_drop else drop_speed
    
    timer += dt
    if timer >= current_speed:
        timer = 0
        if not check_collision(current_piece, current_x, current_y + 1):
            current_y += 1
        else:
            lock_piece()

def draw(grid):
    # Draw Board
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board[y][x]:
                grid[y][x] = 1
                
    if game_over: 
        # Overlay X
        for i in range(8): grid[i][i] = 1; grid[i][7-i] = 1
        return

    # Draw Current Piece
    if current_piece:
        for y, row in enumerate(current_piece):
            for x, val in enumerate(row):
                if val:
                    bx = current_x + x
                    by = current_y + y
                    if 0 <= bx < WIDTH and 0 <= by < HEIGHT:
                        grid[by][bx] = 1
