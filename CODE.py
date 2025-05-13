import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Multiplayer Tic Tac Toe", layout="centered")
st.title("🎮 Multiplayer Tic Tac Toe (2–5 Players, with AI Support)")
if "board" not in st.session_state:
    st.session_state.board = []
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "winner" not in st.session_state:
    st.session_state.winner = None
if "players" not in st.session_state:
    st.session_state.players = []
if "symbols" not in st.session_state:
    st.session_state.symbols = []
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 5
if "ai_enabled" not in st.session_state:
    st.session_state.ai_enabled = []
st.sidebar.header("🎲 Game Setup")
player_count = st.sidebar.slider("Number of Players", 2, 5, 3)
grid_size = st.sidebar.slider("Grid Size", 5, 9, 5)
win_len = st.sidebar.slider("Symbols in a row to Win", 3, min(grid_size, 5), 3)

symbols_default = ['❌', '⭕', '🔺', '🟩', '🟦']
custom_symbols = []
ai_flags = []

for i in range(player_count):
    symbol = st.sidebar.text_input(f"Player {i+1} Symbol", value=symbols_default[i])
    custom_symbols.append(symbol)
    ai_choice = st.sidebar.selectbox(f"Player {i+1} is", ['Human', 'AI'], key=f"ai_option_{i}")
    ai_flags.append(ai_choice == 'AI')

if st.sidebar.button("Start New Game"):
    st.session_state.players = list(range(player_count))
    st.session_state.symbols = custom_symbols
    st.session_state.board = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    st.session_state.turn = 0
    st.session_state.winner = None
    st.session_state.grid_size = grid_size
    st.session_state.ai_enabled = ai_flags
    st.rerun()

def check_winner(board, symbol, win_len):
    n = len(board)

    def check_line(line):
        count = 0
        for cell in line:
            if cell == symbol:
                count += 1
                if count == win_len:
                    return True
            else:
                count = 0
        return False

    for i in range(n):
        if check_line([board[i][j] for j in range(n)]): return True
        if check_line([board[j][i] for j in range(n)]): return True

    for i in range(n - win_len + 1):
        for j in range(n - win_len + 1):
            if all(board[i + k][j + k] == symbol for k in range(win_len)):
                return True
            if all(board[i + k][j + win_len - 1 - k] == symbol for k in range(win_len)):
                return True
    return False

def ai_make_move(symbol):
    empty_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) if st.session_state.board[i][j] == ""]
    if empty_cells:
        i, j = random.choice(empty_cells)
        st.session_state.board[i][j] = symbol
        if check_winner(st.session_state.board, symbol, win_len):
            st.session_state.winner = st.session_state.turn
        else:
            st.session_state.turn = (st.session_state.turn + 1) % player_count
        st.rerun()

if st.session_state.board:
    current_turn = st.session_state.turn
    current_symbol = st.session_state.symbols[current_turn]
    is_ai_turn = st.session_state.ai_enabled[current_turn]

    st.subheader(f"Player {current_turn + 1}'s Turn: {current_symbol} {'🤖' if is_ai_turn else ''}")

    if is_ai_turn and not st.session_state.winner:
        ai_make_move(current_symbol)

    for i in range(grid_size):
        cols = st.columns(grid_size)
        for j in range(grid_size):
            with cols[j]:
                cell_value = st.session_state.board[i][j]
                if cell_value == "":
                    if not is_ai_turn and not st.session_state.winner:
                        if st.button(" ", key=f"{i}-{j}"):
                            st.session_state.board[i][j] = current_symbol
                            if check_winner(st.session_state.board, current_symbol, win_len):
                                st.session_state.winner = current_turn
                            else:
                                st.session_state.turn = (current_turn + 1) % player_count
                            st.rerun()
                else:
                    st.markdown(f"<div style='font-size:28px; text-align:center;'>{cell_value}</div>", unsafe_allow_html=True)

if st.session_state.winner is not None:
    st.success(f"🎉 Player {st.session_state.winner + 1} ({st.session_state.symbols[st.session_state.winner]}) Wins!")

if st.button("🔄 Reset Game"):
    st.session_state.board = [["" for _ in range(grid_size)] for _ in range(grid_size)]
    st.session_state.turn = 0
    st.session_state.winner = None
    st.rerun()