import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="💣 Bomberman Game", layout="centered")
st.title("💣 Streamlit Bomberman - Mini Version")

# Game config
grid_size = 10
explosion_delay = 3  # turns

# Initialize session state
if 'grid' not in st.session_state:
    st.session_state.grid = [['⬜' for _ in range(grid_size)] for _ in range(grid_size)]
    st.session_state.player_pos = [0, 0]
    st.session_state.bombs = []  # list of dicts with keys: pos, timer
    st.session_state.turn = 0

# Helper to render the grid
def render_grid():
    grid_display = st.empty()
    grid_html = "<style>td{text-align:center; font-size:24px; width:40px; height:40px;}</style><table>"
    for row in st.session_state.grid:
        grid_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    grid_html += "</table>"
    grid_display.markdown(grid_html, unsafe_allow_html=True)

# Reset grid
for i in range(grid_size):
    for j in range(grid_size):
        st.session_state.grid[i][j] = '⬜'

# Place static walls
for i in range(2, grid_size, 2):
    for j in range(2, grid_size, 2):
        st.session_state.grid[i][j] = '🟥'

# Place player
px, py = st.session_state.player_pos
st.session_state.grid[px][py] = '😀'

# Place bombs
for bomb in st.session_state.bombs:
    x, y = bomb['pos']
    st.session_state.grid[x][y] = '💣'

# Render grid
render_grid()

# Controls
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬆️ Up"):
        if px > 0 and st.session_state.grid[px - 1][py] == '⬜':
            st.session_state.player_pos[0] -= 1
with col2:
    if st.button("💣 Drop Bomb"):
        st.session_state.bombs.append({"pos": [px, py], "timer": explosion_delay})
with col3:
    if st.button("⬇️ Down"):
        if px < grid_size - 1 and st.session_state.grid[px + 1][py] == '⬜':
            st.session_state.player_pos[0] += 1

col4, _, col5 = st.columns(3)
with col4:
    if st.button("⬅️ Left"):
        if py > 0 and st.session_state.grid[px][py - 1] == '⬜':
            st.session_state.player_pos[1] -= 1
with col5:
    if st.button("➡️ Right"):
        if py < grid_size - 1 and st.session_state.grid[px][py + 1] == '⬜':
            st.session_state.player_pos[1] += 1

# Update bomb timers and handle explosions
explosions = []
for bomb in st.session_state.bombs:
    bomb['timer'] -= 1
    if bomb['timer'] == 0:
        bx, by = bomb['pos']
        explosions.append((bx, by))
        for dx, dy in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = bx + dx, by + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and st.session_state.grid[nx][ny] != '🟥':
                st.session_state.grid[nx][ny] = '💥'

# Remove exploded bombs
st.session_state.bombs = [b for b in st.session_state.bombs if b['timer'] > 0]

# Render updated grid with explosions
time.sleep(0.3)
render_grid()
st.caption("Built with 💣 by ChatGPT using Streamlit")
