# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from time import sleep
#
# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=2, block_orientation=0, rotate=0)
#
# print("Setting brightness...")
# device.contrast(50)
#
# print("Clearing...")
# device.clear()
# sleep(1)
#
# print("Drawing individual pixels...")
# # Draw some pixels directly
# with canvas(device) as draw:
#     # Draw a diagonal line on first matrix
#     for i in range(8):
#         draw.point((i, i), fill="white")
#
# sleep(2)
#
# print("Drawing on second matrix...")
# device.clear()
# sleep(1)
#
# with canvas(device) as draw:
#     # Draw on second matrix (x coordinates 8-15)
#     for i in range(8):
#         draw.point((i + 8, i), fill="white")
#
# sleep(2)
#
# print("Drawing text...")
# device.clear()
# sleep(1)
#
# with canvas(device) as draw:
#     draw.text((0, 0), "HI", fill="white")
#
# sleep(2)
# device.clear()



from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

serial = spi(port=0, device=0, gpio=noop())

# Try different orientations: -90, 0, 90
for orientation in [-90, 0, 90]:
    print(f"Testing orientation: {orientation}")
    device = max7219(serial, cascaded=2, block_orientation=orientation)
    device.contrast(50)

    with canvas(device) as draw:
        draw.text((0, 0), "AB", fill="white")

    sleep(3)
    device.clear()
    sleep(1)
# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from PIL import Image, ImageDraw
# from time import sleep
#
# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=2)
#
# # Create image manually
# img = Image.new('1', (16, 8), 0)  # 16x8 for 2 matrices
# draw = ImageDraw.Draw(img)
#
# # Draw pattern
# draw.rectangle((0, 0, 7, 7), outline=1)
# draw.line((0, 0, 7, 7), fill=1)
#
# # Display it
# device.display(img)
#
# sleep(3)
# device.clear()
# from luma.led_matrix.device import max7219
