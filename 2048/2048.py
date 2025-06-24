import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048 Game", layout="centered")
st.markdown("""
    <style>
        .tile {
            width: 70px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 20px;
            border-radius: 0.3rem;
            color: #776e65;
            margin: 2px; /* Added margin for spacing */
        }
        .board-row {
            display: flex;
            gap: 5px;
            margin-bottom: 5px;
        }
        .board-container {
            width: 310px;
            margin: auto;
        }
        .cell {
            width: 70px;
            height: 70px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("2048 Game")
st.write("Use the arrow keys or buttons to move the tiles. Combine them to reach 2048!")

if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0  # Initialize score
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])

def get_tile_color(val):
    return {
        0: '#cdc1b4', 2: '#eee4da', 4: '#ede0c8',
        8: '#f2b179', 16: '#f59563', 32: '#f67c5f',
        64: '#f65e3b', 128: '#edcf72', 256: '#edcc61',
        512: '#edc850', 1024: '#edc53f', 2048: '#edc22e'
    }.get(val, '#3c3a32')

def draw_board():
    st.markdown('<div class="board-container">', unsafe_allow_html=True)
    for row in st.session_state.grid:
        st.markdown('<div class="board-row">', unsafe_allow_html=True)
        for val in row:
            bg = get_tile_color(val)
            txt = str(val) if val != 0 else ""
            st.markdown(f'<div class="tile" style="background-color: {bg};">{txt}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def add_random_tile():
    empty = list(zip(*np.where(st.session_state.grid == 0)))
    if empty:
        i, j = random.choice(empty)
        st.session_state.grid[i][j] = random.choice([2, 4])

def compress_and_merge(row):
    new = row[row != 0]
    merged = []
    skip = False
    for i in range(len(new)):
        if skip:
            skip = False
            continue
        if i + 1 < len(new) and new[i] == new[i + 1]:
            merged.append(new[i] * 2)
            st.session_state.score += new[i] * 2  # Update score
            skip = True
        else:
            merged.append(new[i])
    return np.array(merged + [0] * (4 - len(merged)))

def move(direction):
    moved = False
    grid = st.session_state.grid.copy()
    for i in range(4):
        if direction == 'left':
            new_row = compress_and_merge(grid[i])
            if not np.array_equal(grid[i], new_row):
                grid[i] = new_row
                moved = True
        elif direction == 'right':
            new_row = compress_and_merge(grid[i][::-1])[::-1]
            if not np.array_equal(grid[i], new_row):
                grid[i] = new_row
                moved = True
        elif direction == 'up':
            new_col = compress_and_merge(grid[:, i])
            if not np.array_equal(grid[:, i], new_col):
                grid[:, i] = new_col
                moved = True
        elif direction == 'down':
            new_col = compress_and_merge(grid[::-1, i])[::-1]
            if not np.array_equal(grid[:, i], new_col):
                grid[:, i] = new_col
                moved = True
    if moved:
        st.session_state.grid = grid
        add_random_tile()
        if check_game_over():  # Check for game over after a move
            st.session_state.game_over = True

def check_game_over():
    if np.any(st.session_state.grid == 0):
        return False
    for i in range(4):
        for j in range(4):
            if (i < 3 and st.session_state.grid[i, j] == st.session_state.grid[i + 1, j]) or \
               (j < 3 and st.session_state.grid[i, j] == st.session_state.grid[i, j + 1]):
                return False
    return True

def reset():
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    st.session_state.game_over = False
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])

cols = st.columns([1, 1, 1, 1])
if cols[0].button("⬅️"):
    move('left')
if cols[1].button("➡️"):
    move('right')
if cols[2].button("⬆️"):
    move('up')
if cols[3].button("⬇️"):
    move('down')

if "game_over" in st.session_state and st.session_state.game_over:
    st.write("Game Over! Your score: ", st.session_state.score)
else:
    st.write("Score: ", st.session_state.score)

st.button("🔁 Restart Game", on_click=reset)

st.markdown("---")
draw_board()
