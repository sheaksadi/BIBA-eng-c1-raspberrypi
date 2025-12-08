import audio
import random

WIDTH = 8
HEIGHT = 16

# State
player_x = 4
bullets = [] # List of [x, y]
enemy_bullets = [] # List of [x, y]
aliens = [] # List of [x, y]
game_over = False
score = 0
direction = 1 # 1=Right, -1=Left
alien_move_timer = 0
alien_speed = 0.5

def init():
    global player_x, bullets, enemy_bullets, aliens, game_over, score, direction, alien_speed
    player_x = 4
    bullets = []
    enemy_bullets = []
    aliens = []
    game_over = False
    score = 0
    direction = 1
    alien_speed = 0.5
    
    # Spawn Aliens
    # 3 Rows of 4 aliens
    for y in range(3):
        for x in range(4):
            aliens.append([x * 2, y * 2 + 1]) # Spread out a bit
            
    audio.play_music('invaders')

def update(dt, inputs):
    global player_x, game_over, alien_move_timer, alien_speed, direction, score
    
    if game_over:
        if inputs['1'] or inputs['2']:
            init()
        return

    # Player Move
    if not hasattr(update, 'last_move'): update.last_move = 0
    update.last_move += dt
    if update.last_move > 0.1:
        if inputs['LEFT'] and player_x > 0:
            player_x -= 1
            update.last_move = 0
        elif inputs['RIGHT'] and player_x < WIDTH - 1:
            player_x += 1
            update.last_move = 0

    # Shoot
    if not hasattr(update, 'last_shot'): update.last_shot = 0
    update.last_shot += dt
    if inputs['UP'] and update.last_shot > 0.5:
        bullets.append([player_x, HEIGHT - 2])
        audio.sfx_shoot()
        update.last_shot = 0
        
    # Update Bullets (Player)
    for b in bullets:
        b[1] -= 1 # Move Up
    # Remove off-screen
    bullets[:] = [b for b in bullets if b[1] >= 0]
    
    # Update Bullets (Enemy)
    for b in enemy_bullets:
        b[1] += 0.5 # Move Down (slower?)
        if b[1] >= HEIGHT:
            b[1] = HEIGHT + 1 # Mark for removal
    enemy_bullets[:] = [b for b in enemy_bullets if b[1] < HEIGHT]

    # Alien Move
    alien_move_timer += dt
    if alien_move_timer >= alien_speed:
        alien_move_timer = 0
        move_aliens()
        
        # Random Alien Shoot
        if aliens and random.random() < 0.2:
            shooter = random.choice(aliens)
            enemy_bullets.append([shooter[0], shooter[1] + 1])
            
    # Collision Logic
    check_collisions()
    
    # Win Condition
    if not aliens:
        # Next Level?
        score += 100
        # Respawn faster
        alien_speed = max(0.1, alien_speed - 0.1)
        # Respawn
        for y in range(3):
            for x in range(4):
                aliens.append([x * 2, y * 2 + 1])
        audio.sfx_select()

def move_aliens():
    global direction, game_over
    # Check edges
    hit_edge = False
    for a in aliens:
        nx = a[0] + direction
        if nx < 0 or nx >= WIDTH:
            hit_edge = True
            break
            
    if hit_edge:
        direction *= -1
        # Move Down
        for a in aliens:
            a[1] += 1
            if a[1] >= HEIGHT - 2: # Reached player level
                game_over = True
                audio.stop_music()
                audio.sfx_crash()
    else:
        for a in aliens:
            a[0] += direction

def check_collisions():
    global score, game_over
    
    # Player Bullet vs Alien
    for b in bullets[:]:
        for a in aliens[:]:
            if int(b[0]) == int(a[0]) and int(b[1]) == int(a[1]):
                if b in bullets: bullets.remove(b)
                if a in aliens: aliens.remove(a)
                score += 10
                audio.sfx_explosion()
                break
                
    # Enemy Bullet vs Player
    for b in enemy_bullets:
        if int(b[0]) == player_x and int(b[1]) == HEIGHT - 1:
            game_over = True
            audio.stop_music()
            audio.sfx_crash()
            
    # Alien Body vs Player
    for a in aliens:
        if int(a[0]) == player_x and int(a[1]) == HEIGHT - 1:
            game_over = True
            audio.stop_music()
            audio.sfx_crash()

def draw(grid):
    # Draw Player
    if not game_over:
        grid[HEIGHT-1][player_x] = 1
    
    # Draw Aliens
    for a in aliens:
        if 0 <= a[1] < HEIGHT and 0 <= a[0] < WIDTH:
            grid[int(a[1])][int(a[0])] = 1
            
    # Draw Bullets
    for b in bullets:
        if 0 <= b[1] < HEIGHT:
            grid[int(b[1])][int(b[0])] = 1
            
    for b in enemy_bullets:
        if 0 <= b[1] < HEIGHT:
            grid[int(b[1])][int(b[0])] = 1

    if game_over:
        # X
        for i in range(8): grid[i][i]=1; grid[i][7-i]=1
