import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="2048 Game", layout="centered")

# CSS styling (same as your original)
st.markdown("""
    <style>
        .game-container {
            width: 100%;
            max-width: 450px;
            margin: 0 auto;
            padding: 20px;
        }
        .board {
            background-color: #bbada0;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            position: relative;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-gap: 15px;
            width: 100%;
        }
        .cell {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            font-weight: bold;
            border-radius: 3px;
            background-color: rgba(238, 228, 218, 0.35);
        }
        .tile-2 { background-color: #eee4da; }
        .tile-4 { background-color: #ede0c8; }
        .tile-8 { background-color: #f2b179; color: white; }
        .tile-16 { background-color: #f59563; color: white; }
        .tile-32 { background-color: #f67c5f; color: white; }
        .tile-64 { background-color: #f65e3b; color: white; }
        .tile-128 { background-color: #edcf72; color: white; font-size: 30px; }
        .tile-256 { background-color: #edcc61; color: white; font-size: 30px; }
        .tile-512 { background-color: #edc850; color: white; font-size: 30px; }
        .tile-1024 { background-color: #edc53f; color: white; font-size: 25px; }
        .tile-2048 { background-color: #edc22e; color: white; font-size: 25px; }
        .controls {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .score-box {
            background: #bbada0;
            padding: 10px 20px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        .game-over {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(238, 228, 218, 0.73);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            z-index: 100;
        }
        .game-over-text {
            font-size: 60px;
            font-weight: bold;
            color: #776e65;
            margin-bottom: 20px;
        }
        @media (max-width: 500px) {
            .board { padding: 10px; }
            .grid-container { grid-gap: 10px; }
            .cell { font-size: 25px; }
            .tile-128, .tile-256, .tile-512 { font-size: 22px; }
            .tile-1024, .tile-2048 { font-size: 18px; }
        }
    </style>
""", unsafe_allow_html=True)

st.title("2048 Game")
st.write("Combine tiles with the same numbers to reach 2048!")

# Initialize game state
if "grid" not in st.session_state:
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    st.session_state.game_over = False
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])


def draw_board():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="controls">
            <div class="score-box">
                <div>SCORE</div>
                <div>{st.session_state.score}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="board">', unsafe_allow_html=True)
    grid_html = '<div class="grid-container">'
    for i in range(4):
        for j in range(4):
            val = st.session_state.grid[i][j]
            tile_class = f"cell tile-{val}" if val > 0 else "cell"
            txt = str(val) if val != 0 else ""
            grid_html += f'<div class="{tile_class}">{txt}</div>'
    grid_html += '</div>'

    if st.session_state.game_over:
        grid_html += f"""
        <div class="game-over">
            <div class="game-over-text">Game Over!</div>
            <div style="font-size: 24px; margin-bottom: 20px;">Score: {st.session_state.score}</div>
        </div>
        """

    st.markdown(grid_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close board
    st.markdown('</div>', unsafe_allow_html=True)  # Close container


def add_random_tile():
    empty = list(zip(*np.where(st.session_state.grid == 0)))
    if empty:
        i, j = random.choice(empty)
        st.session_state.grid[i][j] = random.choice([2, 4])


def compress_and_merge(row):
    new_row = row[row != 0]
    merged = []
    skip = False
    for i in range(len(new_row)):
        if skip:
            skip = False
            continue
        if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
            merged.append(new_row[i] * 2)
            st.session_state.score += new_row[i] * 2
            skip = True
        else:
            merged.append(new_row[i])
    while len(merged) < 4:
        merged.append(0)
    return np.array(merged)


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
        check_game_over()


def check_game_over():
    if np.any(st.session_state.grid == 0):
        st.session_state.game_over = False
        return
    for i in range(4):
        for j in range(4):
            if (i < 3 and st.session_state.grid[i][j] == st.session_state.grid[i + 1][j]) or \
               (j < 3 and st.session_state.grid[i][j] == st.session_state.grid[i][j + 1]):
                st.session_state.game_over = False
                return
    st.session_state.game_over = True


def reset_game():
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    st.session_state.game_over = False
    for _ in range(2):
        i, j = random.choice(list(zip(*np.where(st.session_state.grid == 0))))
        st.session_state.grid[i][j] = random.choice([2, 4])

# Draw UI
draw_board()

col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅️"):
    move("left")
if col2.button("➡️"):
    move("right")
if col3.button("⬆️"):
    move("up")
if col4.button("⬇️"):
    move("down")

if st.button("🔁 New Game"):
    reset_game()
