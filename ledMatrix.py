from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=0)
device.contrast(50)

print("Testing scrolling text...")
# Correct usage: show_message for scrolling
show_message(device, "HELLO", fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)

device.clear()
sleep(1)

print("Testing static text with canvas...")
# For static text, use canvas and draw.text
with canvas(device) as draw:
    # Note: default font is very small, might not show well
    draw.text((0, 0), "HI", fill="white")

sleep(2)
device.clear()

print("Drawing custom letters with pixels...")
# Since text rendering is tricky, let's draw letters manually

def draw_H():
    """Draw letter H on first matrix"""
    with canvas(device) as draw:
        # Left vertical line
        for y in range(8):
            draw.point((1, y), fill="white")
        # Right vertical line
        for y in range(8):
            draw.point((5, y), fill="white")
        # Horizontal middle
        for x in range(1, 6):
            draw.point((x, 3), fill="white")

def draw_I():
    """Draw letter I on second matrix"""
    with canvas(device) as draw:
        # Vertical line
        for y in range(8):
            draw.point((10, y), fill="white")
        # Top horizontal
        for x in range(9, 12):
            draw.point((x, 0), fill="white")
        # Bottom horizontal
        for x in range(9, 12):
            draw.point((x, 7), fill="white")

def draw_HI():
    """Draw HI across both matrices"""
    with canvas(device) as draw:
        # H on first matrix
        for y in range(8):
            draw.point((1, y), fill="white")
            draw.point((5, y), fill="white")
        for x in range(1, 6):
            draw.point((x, 3), fill="white")
        
        # I on second matrix  
        for y in range(8):
            draw.point((10, y), fill="white")
        for x in range(9, 12):
            draw.point((x, 0), fill="white")
            draw.point((x, 7), fill="white")

# Test the custom letters
print("Drawing HI...")
draw_HI()
sleep(3)

device.clear()

# Or try scrolling which usually works better
print("Scrolling message...")
show_message(device, "HELLO WORLD", fill="white", font=proportional(CP437_FONT), scroll_delay=0.04)

device.clear()
print("Done!")
