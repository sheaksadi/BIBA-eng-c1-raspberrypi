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
print("Initializing buttons...")
try:
    btn_up = Button(17, pull_up=True)
    btn_down = Button(27, pull_up=True)
    btn_left = Button(22, pull_up=True)
    btn_right = Button(23, pull_up=True)
    btn_1 = Button(24, pull_up=True)
    btn_2 = Button(25, pull_up=True)
    print("Buttons initialized successfully.")
except Exception as e:
    print(f"Error initializing buttons: {e}")
    print("Ensure you are running with permissions to access GPIO (e.g. sudo).")

def show_text(text_to_show):
    print(f"Button pressed: {text_to_show}")
    # Use canvas for short text to avoid long scrolling delays for simple clicks
    # or show_message for longer text. For single words "UP", "DOWN", canvas is faster.
    with canvas(device) as draw:
        # Simple centering attempt or just draw at 0,0
        # The default font is small, let's just draw it.
        # For better visibility we might want a custom font or just use show_message with fast scroll
        pass
    
    # Let's use show_message for clarity as requested, but make it fast
    show_message(device, text_to_show, fill="white", font=proportional(CP437_FONT), scroll_delay=0.03)

def on_up():
    show_text("UP")

def on_down():
    show_text("DOWN")

def on_left():
    show_text("LEFT")

def on_right():
    show_text("RIGHT")

def on_btn1():
    show_text("1")

def on_btn2():
    show_text("2")

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
