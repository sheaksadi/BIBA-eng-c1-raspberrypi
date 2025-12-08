from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
import threading

# Constants
PIN_BUZZER = 18

buzzer = None
enabled = False

# Music State
current_track = None
music_thread = None
stop_event = threading.Event()
sfx_lock = threading.Lock()

# Melodies (Note, Duration in seconds)
# Tetris Theme A (Korobeiniki) simplified
TETRIS_THEME = [
    ('E5', 0.2), ('B4', 0.1), ('C5', 0.1), ('D5', 0.2), ('C5', 0.1), ('B4', 0.1),
    ('A4', 0.2), ('A4', 0.1), ('C5', 0.1), ('E5', 0.2), ('D5', 0.1), ('C5', 0.1),
    ('B4', 0.2), ('B4', 0.1), ('C5', 0.1), ('D5', 0.2), ('E5', 0.2),
    ('C5', 0.2), ('A4', 0.2), ('A4', 0.4),
    # Bridge
    ('D5', 0.2), ('F5', 0.1), ('A5', 0.2), ('G5', 0.1), ('F5', 0.1),
    ('E5', 0.3), ('C5', 0.1), ('E5', 0.2), ('D5', 0.1), ('C5', 0.1),
    ('B4', 0.2), ('B4', 0.1), ('C5', 0.1), ('D5', 0.2), ('E5', 0.2),
    ('C5', 0.2), ('A4', 0.2), ('A4', 0.4)
]

# Simple Snake Tune (Fast paced loop)
SNAKE_THEME = [
    ('C4', 0.1), ('E4', 0.1), ('G4', 0.1),
    ('A4', 0.1), ('G4', 0.1), ('E4', 0.1),
    ('C4', 0.1), ('E4', 0.1), ('G4', 0.1),
    ('B3', 0.1), ('D4', 0.1), ('G4', 0.1),
    ('F4', 0.1), ('D4', 0.1), ('B3', 0.1),
    ('G3', 0.3)
]

TRACKS = {
    'tetris': TETRIS_THEME,
    'snake': SNAKE_THEME
}

def init():
    global buzzer, enabled
    try:
        buzzer = TonalBuzzer(PIN_BUZZER)
        enabled = True
        print("Audio initialized on GPIO", PIN_BUZZER)
    except Exception as e:
        print(f"Audio init failed: {e}")
        enabled = False

def play_music(track_name):
    global current_track, music_thread, stop_event
    if not enabled: return
    
    stop_music()
    
    if track_name in TRACKS:
        current_track = TRACKS[track_name]
        stop_event.clear()
        music_thread = threading.Thread(target=_music_loop, daemon=True)
        music_thread.start()

def stop_music():
    global stop_event, music_thread
    if music_thread and music_thread.is_alive():
        stop_event.set()
        music_thread.join(timeout=0.2)
    
    if buzzer:
        buzzer.stop()

def _music_loop():
    idx = 0
    track = current_track
    while not stop_event.is_set() and track:
        note, duration = track[idx]
        
        # Only play if SFX isn't locking
        with sfx_lock:
            try:
                buzzer.play(Tone(note))
            except: pass
            
        # Wait for duration
        # We check stop_event frequently for responsiveness
        end_time = time.time() + duration * 0.9 # Little gap between notes
        while time.time() < end_time:
            if stop_event.is_set(): return
            time.sleep(0.01)
            
        # Brief silence between notes for articulation
        with sfx_lock:
            try:
                buzzer.stop()
            except: pass
        time.sleep(duration * 0.1)
            
        idx = (idx + 1) % len(track)

def play_tone(frequency, duration):
    if not enabled or not buzzer: return
    
    def _t():
        # Acquire lock to pause music writing to buzzer (music thread will just wait/sleep)
        # Note: Ideally music thread pauses, but here we just overwrite
        # Locking ensures we don't interleave commands too fast
        with sfx_lock: 
            try:
                buzzer.play(Tone(frequency))
            except: pass
            
        time.sleep(duration)
        
        with sfx_lock:
            try:
                buzzer.stop()
            except: pass
            
    threading.Thread(target=_t, daemon=True).start()

# Sound Effects (frequencies approx)
def sfx_move(): play_tone(440, 0.05)       # A4
def sfx_rotate(): play_tone(523.25, 0.05)  # C5
def sfx_drop(): play_tone(220, 0.1)        # A3
def sfx_eat(): play_tone(659.25, 0.1)      # E5
def sfx_crash(): play_tone(110, 0.5)       # A2
def sfx_line(): 
    if not enabled: return
    def _t():
        with sfx_lock:
            buzzer.play(Tone(523.25))
        time.sleep(0.1)
        with sfx_lock:
            buzzer.play(Tone(659.25))
        time.sleep(0.1)
        with sfx_lock:
            buzzer.play(Tone(783.99))
        time.sleep(0.2)
        with sfx_lock:
            buzzer.stop()
    threading.Thread(target=_t, daemon=True).start()

def sfx_select(): play_tone(880, 0.1)
