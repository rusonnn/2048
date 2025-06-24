import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048", layout="centered")
st.title("2048 Game")

# Initialize game state
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])


def draw_board():
    for row in st.session_state.grid:
        cols = st.columns(4)
        for i, val in enumerate(row):
            tile_style = f"background-color: {get_color(val)}; height: 100px; border-radius: 10px; text-align: center; font-size: 32px; line-height: 100px; color: {get_font_color(val)};"
            cols[i].markdown(f"<div style='{tile_style}'>{val if val != 0 else ''}</div>", unsafe_allow_html=True)


def get_color(value):
    return {
        0: '#cdc1b4', 2: '#eee4da', 4: '#ede0c8',
        8: '#f2b179', 16: '#f59563', 32: '#f67c5f', 64: '#f65e3b',
        128: '#edcf72', 256: '#edcc61', 512: '#edc850',
        1024: '#edc53f', 2048: '#edc22e'
    }.get(value, '#3c3a32')


def get_font_color(value):
    return '#776e65' if value <= 4 else '#f9f6f2'


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


col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅️"):
    move('left')
if col2.button("➡️"):
    move('right')
if col3.button("⬆️"):
    move('up')
if col4.button("⬇️"):
    move('down')

if st.button("🔁 Restart"):
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])

st.write("""
Use the arrow buttons to play. Your goal is to reach **2048**! 🎯
""")

st.markdown("---")
draw_board()
