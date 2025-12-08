# audio.py Updates
1. **Define Melodies**:
   - `TETRIS_THEME`: List of `(note, duration)` tuples.
   - `SNAKE_THEME`: List of `(note, duration)` tuples.
2. **Music Loop**:
   - A daemon thread that iterates through the current melody.
   - Checks `current_track` global.
   - Handles `stop_music`.
3. **Conflict Resolution**:
   - `sfx_*` functions currently `play()`, `sleep()`, `stop()`.
   - `stop()` kills the PWM.
   - If music is running, `stop()` creates silence.
   - Enhancement: `sfx` sets a `sfx_playing` flag? Or music thread re-asserts tone? 
   - Simple approach: Just loop. If SFX cuts it, so be it.

# Game Updates
- **main.py**:
  - `update_menu`: `audio.stop_music()` (or play Menu theme?)
  - When starting game: `audio.play_music('snake')` or `audio.play_music('tetris')`.
- **snake.py**:
  - `init`: `audio.play_music('snake')`.
  - `game_over`: `audio.stop_music()`.
- **tetris.py**:
  - `init`: `audio.play_music('tetris')`.
  - `game_over`: `audio.stop_music()`.
