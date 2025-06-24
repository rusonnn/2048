import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048 Game", layout="centered")
st.markdown("""
    <style>
        .tile {
            width: 100%;
            aspect-ratio: 1 / 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 6vw;
            border-radius: 0.5rem;
            color: #776e65;
        }
        .board-row {
            display: flex;
            gap: 1vw;
            margin-bottom: 1vw;
        }
        .board-container {
            max-width: 90vw;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("2048 (Responsive)")

if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((4, 4), dtype=int)
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
        cols = st.columns(4)
        for i, val in enumerate(row):
            bg = get_tile_color(val)
            txt = str(val) if val != 0 else ""
            cols[i].markdown(f'<div class="tile" style="background-color: {bg};">{txt}</div>', unsafe_allow_html=True)
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
            new_row = compress_and_merge(grid[:, i])
            if not np.array_equal(grid[:, i], new_row):
                grid[:, i] = new_row
                moved = True
        elif direction == 'down':
            new_row = compress_and_merge(grid[::-1, i])[::-1]
            if not np.array_equal(grid[:, i], new_row):
                grid[:, i] = new_row
                moved = True
    if moved:
        st.session_state.grid = grid
        add_random_tile()


def reset():
    st.session_state.grid = np.zeros((4, 4), dtype=int)
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

st.button("🔁 Restart Game", on_click=reset)

st.markdown("---")
draw_board()
