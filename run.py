import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from gpiozero import Button
from signal import pause
import sys

# Import the game logic
import main

# --- Hardware Setup ---
print("Initializing Hardware...")

# LED Matrix
try:
    serial = spi(port=0, device=0, gpio=noop())
    # Note: cascaded=2 gives a 16x8 canvas (Width=16, Height=8) usually, 
    # but depends on physical orientation.
    # We will map our logical grid to this Luma canvas.
    device = max7219(serial, cascaded=2, block_orientation=0)
    device.contrast(50)
except Exception as e:
    print(f"Error initializing LED Matrix: {e}")
    sys.exit(1)

# Buttons
# Active Low: Pressed = 0 (Ground), Released = 1 (3.3V)
# pull_up=True enables internal resistor.
buttons_map = {
    'UP': Button(17, pull_up=True, bounce_time=0.01),
    'DOWN': Button(27, pull_up=True, bounce_time=0.01),
    'LEFT': Button(22, pull_up=True, bounce_time=0.01),
    'RIGHT': Button(23, pull_up=True, bounce_time=0.01),
    '1': Button(24, pull_up=True, bounce_time=0.01),
    '2': Button(25, pull_up=True, bounce_time=0.01)
}

def get_inputs():
    """Reads all buttons and returns a dictionary of their states."""
    inputs = {}
    for name, btn in buttons_map.items():
        inputs[name] = btn.is_pressed
    return inputs

def render_grid_to_device(grid):
    """
    Maps the logical 8x16 grid (grid[y][x]) to the Luma 16x8 canvas.
    
    Correction Logic (based on User feedback):
    - Device 0 (Bottom Screen) should show Logical Rows 8-15.
    - Device 1 (Top Screen) should show Logical Rows 0-7.
    
    Luma Chaining:
    - Typically Device 0 is x=0..7, Device 1 is x=8..15.
    
    So:
    - Logical y in 8..15 -> Device 0 (x=0..7). Map x->x, y->(y-8).
    - Logical y in 0..7  -> Device 1 (x=8..15). Map x->(x+8), y->y.
    """
    
    with canvas(device) as draw:
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x]:
                    if y < 8:
                        # Top Screen (Device 1)
                        # Map logical x to x+8 (second block)
                        phys_x = x + 8
                        phys_y = y
                    else:
                        # Bottom Screen (Device 0)
                        # Map logical x to x (first block)
                        # Map logical y to y-8 (relative to block)
                        phys_x = x
                        phys_y = y - 8
                        
                    # Safety check
                    if 0 <= phys_x < 16 and 0 <= phys_y < 8:
                        draw.point((phys_x, phys_y), fill="white")

def run_game():
    print("Starting Game Loop...")
    main.init()
    
    last_time = time.time()
    
    try:
        while True:
            # Time delta
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Input
            inputs = get_inputs()
            
            # Update
            main.update(dt, inputs)
            
            # Draw (Update Grid)
            main.draw()
            
            # Render to Hardware
            render_grid_to_device(main.grid)
            
            # Cap Frame Rate (~60 FPS)
            time.sleep(0.016)
            
    except KeyboardInterrupt:
        print("\nExiting...")
        device.cleanup() # If method exists, else safe to just exit
        sys.exit(0)

if __name__ == "__main__":
    run_game()
