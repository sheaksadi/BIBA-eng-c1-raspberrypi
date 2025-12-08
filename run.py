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
    
    Correction Logic V2:
    - User says '1' (Top Logical) appeared on Bottom Screen -> Previous mapping was inverted.
      - Previous: Top->Device 1, Bottom->Device 0.
      - New: Top->Device 0 (Phys X 0..7), Bottom->Device 1 (Phys X 8..15).
    - User says "Mirrored" -> Needs 'flipped'.
      - Since we swapped axes for rotation, mapping Logical X to Phys Y.
      - Invert Phys Y: 7 - logical_x.
    
    Simplified Mapping:
    - Logical Y (0..15) -> Physical X (0..15).
    - Logical X (0..7)  -> Physical Y (0..7) inverted.
    """
    
    with canvas(device) as draw:
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x]:
                    # Axis Swap + Global Mapping
                    # Assuming the chain aligns perfectly with Y-axis now.
                    phys_x = y
                    phys_y = 7 - x
                        
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
