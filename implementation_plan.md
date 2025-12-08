# Hardware Changes
- Add Buzzer to **GPIO 18** (PWM capable).

# Software Changes
## 1. New File: `audio.py`
- Uses `gpiozero.TonalBuzzer`.
- Defines sounds: `SND_MOVE`, `SND_ROTATE`, `SND_EAT`, `SND_CRASH`, `SND_LINE`, `SND_LEVELUP`.
- Simple queue or fire-and-forget interface.

## 2. Update `run.py`
- Initialize `audio.py`.
- In main loop, process audio queue (if needed) or let `gpiozero` handle background.

## 3. Update `snake.py`
- **Speed**: Change `SPEED` from 0.15 to **0.25** or **0.3**.
- **Sound**: Play `SND_EAT` when food eaten, `SND_CRASH` on game over.

## 4. Update `tetris.py`
- **Rotation Fix**: Implement `prev_up` state to detect *rising edge* of the button press. Only rotate once per press.
- **Sound**: Play `SND_ROTATE`, `SND_MOVE`, `SND_DROP`, `SND_LINE`.

## 5. Update `main.py`
- Menu navigation sounds.
- Pass audio context to games? Or `audio.play()` is global? 
- Impl: `import audio` in games is easiest if `audio.init(pin)` is called in `run.py`.
