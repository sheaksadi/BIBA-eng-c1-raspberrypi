from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

# Setup (cascaded=2 because you have 2 matrices)
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=0)

# Simple test pattern
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white")
    draw.text((2, 0), "Hi", fill="white")
