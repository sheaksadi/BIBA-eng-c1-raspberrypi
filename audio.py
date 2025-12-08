from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
import threading

# Constants
PIN_BUZZER = 18

buzzer = None
enabled = False

def init():
    global buzzer, enabled
    try:
        buzzer = TonalBuzzer(PIN_BUZZER)
        enabled = True
        print("Audio initialized on GPIO", PIN_BUZZER)
    except Exception as e:
        print(f"Audio init failed: {e}")
        enabled = False

def play_tone(frequency, duration):
    if not enabled or not buzzer: return
    
    # Run in a thread to not block game loop
    def _t():
        try:
            buzzer.play(Tone(frequency))
            time.sleep(duration)
            buzzer.stop()
        except:
            pass
    threading.Thread(target=_t, daemon=True).start()

# Sound Effects
def sfx_move(): play_tone(440, 0.05)       # A4
def sfx_rotate(): play_tone(523.25, 0.05)  # C5
def sfx_drop(): play_tone(220, 0.1)        # A3
def sfx_eat(): play_tone(659.25, 0.1)      # E5
def sfx_crash(): play_tone(110, 0.5)       # A2
def sfx_line(): 
    # Arpeggio
    if not enabled: return
    def _t():
        buzzer.play(Tone(523.25)); time.sleep(0.1)
        buzzer.play(Tone(659.25)); time.sleep(0.1)
        buzzer.play(Tone(783.99)); time.sleep(0.2)
        buzzer.stop()
    threading.Thread(target=_t, daemon=True).start()

def sfx_select(): play_tone(880, 0.1)
