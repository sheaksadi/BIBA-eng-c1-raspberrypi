# Architecture
- main.py:
    - State Machine (MENU, SNAKE, TETRIS)
    - Shared Grid (8x16)
    - update(): delegates to current_state.update()
    - draw(): clears grid, delegates to current_state.draw(grid)

- snake.py:
    - Standard Snake Logic
    - Input: D-Pad
    - Fail Condition: Wall or Self collision -> State: GameOver -> Any Key -> Reset

- tetris.py:
    - 8x16 Board
    - Standard Shapes (I, O, T, S, Z, J, L)
    - Input: Left/Right (Move), Up (Rotate), Down (Fast Drop)
    - Line clearing
    - Fail Condition: Top out

# main.py Menu
- "1" -> Tetris
- "2" -> Snake
- Display "T" or "S" or "1"/"2" via bitmaps to indicate choice.

# File Operations
1. Create snake.py
2. Create tetris.py
3. Modify main.py
