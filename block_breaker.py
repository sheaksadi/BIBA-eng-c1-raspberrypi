import audio

WIDTH = 8
HEIGHT = 16

# Game State
paddle_x = 3
paddle_width = 3
ball_x = 4.0
ball_y = 12.0
ball_dx = 1.0
ball_dy = -1.0
ball_speed = 0.1
blocks = []
game_over = False
win = False
score = 0
timer = 0

def init():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, blocks, game_over, win, score, timer
    paddle_x = 3
    ball_x = 4.0
    ball_y = 12.0
    ball_dx = 1.0
    ball_dy = -1.0
    game_over = False
    win = False
    score = 0
    timer = 0
    
    # Create blocks (top 4 rows)
    blocks = []
    for y in range(4):
        for x in range(WIDTH):
            blocks.append([x, y])
    
    audio.play_music('breakout')

def update(dt, inputs):
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, game_over, win, score, timer
    
    if game_over or win:
        if inputs['1']:
            init()
        return

    # Paddle Movement
    if inputs['LEFT'] and paddle_x > 0:
        paddle_x -= 1
    elif inputs['RIGHT'] and paddle_x < WIDTH - paddle_width:
        paddle_x += 1

    # Ball Update
    timer += dt
    if timer >= ball_speed:
        timer = 0
        
        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Wall Bounce (Left/Right)
        if ball_x < 0:
            ball_x = 0
            ball_dx = abs(ball_dx)
            audio.sfx_move()
        elif ball_x >= WIDTH:
            ball_x = WIDTH - 1
            ball_dx = -abs(ball_dx)
            audio.sfx_move()
            
        # Top Bounce
        if ball_y < 0:
            ball_y = 0
            ball_dy = abs(ball_dy)
            audio.sfx_move()
            
        # Bottom (Miss)
        if ball_y >= HEIGHT:
            game_over = True
            audio.stop_music()
            audio.sfx_crash()
            return
            
        # Paddle Bounce
        if int(ball_y) == HEIGHT - 2:
            if paddle_x <= int(ball_x) < paddle_x + paddle_width:
                ball_dy = -abs(ball_dy)
                # Angle based on where it hits paddle
                hit_pos = int(ball_x) - paddle_x
                if hit_pos == 0:
                    ball_dx = -1.5
                elif hit_pos == paddle_width - 1:
                    ball_dx = 1.5
                else:
                    ball_dx = ball_dx * 0.8  # Slight dampen
                audio.sfx_rotate()
                
        # Block Collision
        bx, by = int(ball_x), int(ball_y)
        for block in blocks[:]:
            if block[0] == bx and block[1] == by:
                blocks.remove(block)
                ball_dy = -ball_dy
                score += 10
                audio.sfx_eat()
                break
                
        # Win Condition
        if not blocks:
            win = True
            audio.stop_music()
            audio.sfx_select()

def draw(grid):
    # Draw Blocks
    for block in blocks:
        x, y = block
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = 1
            
    # Draw Ball
    bx, by = int(ball_x), int(ball_y)
    if 0 <= bx < WIDTH and 0 <= by < HEIGHT:
        grid[by][bx] = 1
        
    # Draw Paddle
    paddle_y = HEIGHT - 1
    for i in range(paddle_width):
        px = paddle_x + i
        if 0 <= px < WIDTH:
            grid[paddle_y][px] = 1
            
    if game_over:
        # X pattern
        for i in range(8):
            grid[4+i][i] = 1
            grid[4+i][7-i] = 1
    elif win:
        # Checkmark / happy face?
        grid[6][2] = 1; grid[7][3] = 1; grid[6][4] = 1; grid[5][5] = 1
