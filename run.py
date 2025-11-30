from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT
from gpiozero import Button
from time import sleep
from signal import pause

# LED Matrix Setup
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=0)
device.contrast(50)

# Button Setup
# UP: 17, DOWN: 27, LEFT: 22, RIGHT: 23, 1: 24, 2: 25
# Connect one side of button to GPIO, other side to Ground.
# pull_up=True means internal resistor pulls to 3.3V, pressing button connects to Ground (0V).
# Button Setup
# UP: 17, DOWN: 27, LEFT: 22, RIGHT: 23, 1: 24, 2: 25
# Button Setup
# UP: 17, DOWN: 27, LEFT: 22, RIGHT: 23, 1: 24, 2: 25
# Connect one side of button to GPIO, other side to Ground.
# pull_up=True means internal resistor pulls to 3.3V, pressing button connects to Ground (0V).
print("Initializing buttons (Active Low - Connect to Ground)...")
# Added bounce_time to filter noise
btn_up = Button(17, pull_up=True, bounce_time=0.1)
btn_down = Button(27, pull_up=True, bounce_time=0.1)
btn_left = Button(22, pull_up=True, bounce_time=0.1)
btn_right = Button(23, pull_up=True, bounce_time=0.1)
btn_1 = Button(24, pull_up=True, bounce_time=0.1)
btn_2 = Button(25, pull_up=True, bounce_time=0.1)
print("Buttons initialized successfully.")

def draw_arrow(direction):
    print(f"Button pressed: {direction}")
    with canvas(device) as draw:
        if direction == "UP":
            # Draw Up Arrow
            draw.line((3, 7, 3, 0), fill="white")
            draw.line((3, 0, 0, 3), fill="white")
            draw.line((3, 0, 6, 3), fill="white")
        elif direction == "DOWN":
            # Draw Down Arrow
            draw.line((3, 0, 3, 7), fill="white")
            draw.line((3, 7, 0, 4), fill="white")
            draw.line((3, 7, 6, 4), fill="white")
        elif direction == "LEFT":
            # Draw Left Arrow
            draw.line((7, 3, 0, 3), fill="white")
            draw.line((0, 3, 3, 0), fill="white")
            draw.line((0, 3, 3, 6), fill="white")
        elif direction == "RIGHT":
            # Draw Right Arrow
            draw.line((0, 3, 7, 3), fill="white")
            draw.line((7, 3, 4, 0), fill="white")
            draw.line((7, 3, 4, 6), fill="white")
        elif direction == "1":
            draw.text((0, 0), "1", fill="white")
        elif direction == "2":
            draw.text((0, 0), "2", fill="white")
    
    # Keep the arrow on screen for a moment
    sleep(0.5)
    device.clear()

def on_up():
    draw_arrow("UP")

def on_down():
    draw_arrow("DOWN")

def on_left():
    draw_arrow("LEFT")

def on_right():
    draw_arrow("RIGHT")

def on_btn1():
    draw_arrow("1")

def on_btn2():
    draw_arrow("2")

# Assign callbacks
btn_up.when_pressed = on_up
btn_down.when_pressed = on_down
btn_left.when_pressed = on_left
btn_right.when_pressed = on_right
btn_1.when_pressed = on_btn1
btn_2.when_pressed = on_btn2

print("Button monitor started. Press buttons...")
show_message(device, "READY", fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)

# Keep script running
pause()
