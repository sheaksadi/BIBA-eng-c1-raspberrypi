from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=0)
device.contrast(50)

print("Testing with built-in fonts...")

# Method 1: Using legacy text function (works better for LED matrices)
text(device, "HI", fill="white", font=proportional(CP437_FONT))
sleep(2)

device.clear()
sleep(1)

# Method 2: Scrolling text
print("Scrolling text...")
show_message(device, "HELLO", fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)

device.clear()
sleep(1)

# Method 3: Drawing patterns that definitely work
print("Drawing patterns...")
with canvas(device) as draw:
    # First matrix - checkerboard
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            draw.point((x, y), fill="white")
            draw.point((x+1, y+1), fill="white")
    
    # Second matrix - diagonal lines
    for i in range(8):
        draw.point((i + 8, i), fill="white")
        draw.point((i + 8, 7 - i), fill="white")

sleep(3)
device.clear()

print("Done!")
