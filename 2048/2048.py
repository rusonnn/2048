import streamlit as st
import numpy as np
import random

# Initialize session state variables
if 'grid' not in st.session_state:
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    st.session_state.game_over = False
    # Add two initial tiles
    for _ in range(2):
        empty_cells = list(zip(*np.where(st.session_state.grid == 0)))
        if empty_cells:
            i, j = random.choice(empty_cells)
            st.session_state.grid[i][j] = random.choice([2, 4])

# Configure page
st.set_page_config(page_title="2048 Game", layout="centered")

# CSS styling for the game
st.markdown("""
    <style>
        .game-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
        }
        .board {
            background-color: #bbada0;
            border-radius: 6px;
            width: 100%;
            max-width: 450px;
            padding: 15px;
            margin: 0 auto 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-gap: 15px;
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
        
        @media (max-width: 500px) {
            .board { padding: 10px; grid-gap: 10px; }
            .cell { font-size: 25px; }
            .tile-128, 
            .tile-256, 
            .tile-512 { font-size: 22px; }
        }
        
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
            text-align: center;
        }
        .button-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        .game-over {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(238, 228, 218, 0.8);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

def draw_board():
    with st.container():
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        
        # Score display
        st.markdown(f"""
            <div class="controls">
                <div class="score-box">
                    <div>SCORE</div>
                    <div style="font-size: 24px; font-weight: bold;">{st.session_state.score}</div>
                </div>
                <button onclick="window.streamlitNativeAPI.showModal('Restart Game')" 
                    style="background: #8f7a66; color: white; border: none; 
                    border-radius: 5px; padding: 10px 20px; font-weight: bold;">
                    New Game
                </button>
            </div>
        """, unsafe_allow_html=True)
        
        # Game board
        st.markdown('<div class="board">', unsafe_allow_html=True)
        st.markdown('<div class="grid">', unsafe_allow_html=True)
        
        for i in range(4):
            for j in range(4):
                val = st.session_state.grid[i][j]
                tile_class = f"cell tile-{val}" if val > 0 else "cell"
                txt = str(val) if val != 0 else ""
                st.markdown(f'<div class="{tile_class}">{txt}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close grid
        st.markdown('</div>', unsafe_allow_html=True)  # Close board
        
        # Direction buttons
        st.markdown("""
            <div class="button-row">
                <button onclick="moveDirection('left')">⬅️ Left</button>
                <button onclick="moveDirection('right')">➡️ Right</button>
                <button onclick="moveDirection('up')">⬆️ Up</button>
                <button onclick="moveDirection('down')">⬇️ Down</button>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close game-container

        # Game over overlay if needed
        if st.session_state.game_over:
            st.markdown("""
                <div class="game-over">
                    Game Over!<br>
                    Final Score: """ + str(st.session_state.score) + """<br>
                    <button onclick="resetGame()" style="margin-top: 10px;">Try Again</button>
                </div>
            """, unsafe_allow_html=True)

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
            st.session_state.score += new_row[i] * 2  # Update score
            skip = True
        else:
            merged.append(new_row[i])
    
    # Fill remaining spaces with zeros
    while len(merged) < 4:
        merged.append(0)
    
    return np.array(merged)

def move(direction):
    old_grid = st.session_state.grid.copy()
    moved = False
    
    if direction == 'left':
        for i in range(4):
            new_row = compress_and_merge(st.session_state.grid[i])
            if not np.array_equal(st.session_state.grid[i], new_row):
                st.session_state.grid[i] = new_row
                moved = True
    
    elif direction == 'right':
        for i in range(4):
            new_row = compress_and_merge(st.session_state.grid[i][::-1])[::-1]
            if not np.array_equal(st.session_state.grid[i], new_row):
                st.session_state.grid[i] = new_row
                moved = True
    
    elif direction == 'up':
        for j in range(4):
            new_col = compress_and_merge(st.session_state.grid[:, j])
            if not np.array_equal(st.session_state.grid[:, j], new_col):
                st.session_state.grid[:, j] = new_col
                moved = True
    
    elif direction == 'down':
        for j in range(4):
            new_col = compress_and_merge(st.session_state.grid[::-1, j])[::-1]
            if not np.array_equal(st.session_state.grid[:, j], new_col):
                st.session_state.grid[:, j] = new_col
                moved = True
    
    if moved:
        # Update the Board component manually
        st.toast("Move successful!")
        
        # Add new random tile
        if not st.session_state.game_over:
            empty_cells = list(zip(*np.where(st.session_state.grid == 0)))
            if empty_cells:
                i, j = random.choice(empty_cells)
                st.session_state.grid[i][j] = random.choice([2, 4])
    
    # Check game over condition after move
    check_game_over()

def check_game_over():
    if np.any(st.session_state.grid == 0):
        st.session_state.game_over = False
        return
    
    # Check for possible merges
    for i in range(4):
        for j in range(4):
            if (i < 3 and st.session_state.grid[i][j] == st.session_state.grid[i+1][j]) or \
               (j < 3 and st.session_state.grid[i][j] == st.session_state.grid[i][j+1]):
                st.session_state.game_over = False
                return
    
    st.session_state.game_over = True

st.title("2048 Game")

# Draw the initial board
draw_board()

# JavaScript handlers for buttons
st.markdown("""
    <script>
    function moveDirection(direction) {
        Streamlit.setComponentValue({"direction": direction})
    }
    
    function resetGame() {
        Streamlit.setComponentValue({"reset": true})
    }
    </script>
""", unsafe_allow_html=True)

# Handle button clicks
if st.session_state.get('_components', {}).get('value', {}).get('direction'):
    direction = st.session_state._components.value.direction
    move(direction)
    st.session_state._components.value.direction = None

if st.session_state.get('_components', {}).get('value', {}).get('reset'):
    st.session_state.grid = np.zeros((4, 4), dtype=int)
    st.session_state.score = 0
    st.session_state.game_over = False
    # Add two initial tiles
    for _ in range(2):
        empty_cells = list(zip(*np.where(st.session_state.grid == 0)))
        if empty_cells:
            i, j = random.choice(empty_cells)
            st.session_state.grid[i][j] = random.choice([2, 4])
    st.session_state._components.value.reset = None
