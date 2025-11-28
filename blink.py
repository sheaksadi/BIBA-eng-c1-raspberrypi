import RPi.GPIO as GPIO
import time

# LED Configuration
LED_PIN = 17  # GPIO pin number (BCM mode) - change this to match your wiring

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(LED_PIN, GPIO.OUT)
    print(f"LED connected to GPIO {LED_PIN}")
    print("Starting blink test...")

def blink(duration=0.5, count=10):
    """
    Blink the LED
    
    Args:
        duration: How long LED stays on/off (seconds)
        count: Number of blinks (0 = infinite)
    """
    try:
        iterations = 0
        while count == 0 or iterations < count:
            GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
            print("LED ON")
            time.sleep(duration)
            
            GPIO.output(LED_PIN, GPIO.LOW)   # LED OFF
            print("LED OFF")
            time.sleep(duration)
            
            iterations += 1
            
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    setup()
    blink(duration=0.5, count=10)  # Blink 10 times, 0.5s on/off
    # blink(duration=1, count=0)   # Uncomment for infinite blinking
