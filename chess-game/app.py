import random
from typing import List, Optional

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    import chess
    import chess.svg
except ImportError as exc:  # pragma: no cover - instructions for missing deps
    raise RuntimeError(
        "python-chess is required. Install it with `pip install streamlit python-chess pandas`."
    ) from exc


# -----------------------------------------------------------------------------
# Session helpers
# -----------------------------------------------------------------------------

def init_state():
    if "board" not in st.session_state:
        st.session_state.board = chess.Board()
    if "move_history" not in st.session_state:
        st.session_state.move_history: List[str] = []
    if "player_is_white" not in st.session_state:
        st.session_state.player_is_white = True
    if "ai_enabled" not in st.session_state:
        st.session_state.ai_enabled = True
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""
    st.session_state.setdefault("promotion_choice", "Queen")
    st.session_state.setdefault("selected_square", None)


def reset_game(player_color: Optional[str] = None):
    st.session_state.board = chess.Board()
    st.session_state.move_history = []
    if player_color is not None:
        st.session_state.player_is_white = player_color == "White"
    st.session_state.status_message = "New game started."
    if st.session_state.ai_enabled and not st.session_state.player_is_white:
        trigger_ai_move()


# -----------------------------------------------------------------------------
# Rendering utilities
# -----------------------------------------------------------------------------

def render_board():
    board = st.session_state.board
    orientation = chess.WHITE if st.session_state.player_is_white else chess.BLACK
    highlight = board.king(board.turn) if board.is_check() else None
    last_move = board.move_stack[-1] if board.move_stack else None
    svg = chess.svg.board(board, orientation=orientation, lastmove=last_move, check=highlight, size=480)
    html = f"""
        <style>
            .board-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 0.5rem;
            }}
            .board-container svg {{
                max-width: 100%;
                height: auto;
            }}
        </style>
        <div class="board-container">{svg}</div>
    """
    components.html(html, height=620)


def render_click_grid():
    board = st.session_state.board
    orientation_white = st.session_state.player_is_white
    ranks = list(range(7, -1, -1)) if orientation_white else list(range(8))
    files = list(range(8)) if orientation_white else list(range(7, -1, -1))

    st.markdown("#### Click a piece, then its destination")
    for rank in ranks:
        cols = st.columns(8, gap="small")
        for idx, file_index in enumerate(files):
            square = chess.square(file_index, rank)
            piece = board.piece_at(square)
            square_name = chess.square_name(square)
            symbol = piece.unicode_symbol() if piece else "·"
            label = f"{symbol}\n{square_name.upper()}"
            if st.session_state.selected_square == square_name:
                label = f"➤ {label}"
            button_key = f"square_{square_name}"
            if cols[idx].button(label, key=button_key):
                handle_square_click(square_name)
        st.write("")


def show_move_history():
    moves = st.session_state.move_history
    rows = []
    for idx in range(0, len(moves), 2):
        rows.append(
            {
                "Move": idx // 2 + 1,
                "White": moves[idx],
                "Black": moves[idx + 1] if idx + 1 < len(moves) else "",
            }
        )
    if rows:
        st.table(pd.DataFrame(rows).set_index("Move"))
    else:
        st.info("No moves yet. Enter a move using SAN (`e4`) or UCI (`e2e4`).")


# -----------------------------------------------------------------------------
# Game logic
# -----------------------------------------------------------------------------

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

PROMOTION_LETTER_MAP = {
    "queen": "q",
    "rook": "r",
    "bishop": "b",
    "knight": "n",
}


def evaluate_board(board: chess.Board, perspective: bool) -> float:
    white_score = sum(PIECE_VALUES[p.piece_type] for p in board.piece_map().values() if p.color == chess.WHITE)
    black_score = sum(PIECE_VALUES[p.piece_type] for p in board.piece_map().values() if p.color == chess.BLACK)
    total = white_score - black_score
    return total if perspective == chess.WHITE else -total


def choose_ai_move(board: chess.Board) -> chess.Move:
    perspective = board.turn
    best_score = -float("inf")
    best_moves: List[chess.Move] = []

    for move in board.legal_moves:
        board.push(move)
        score = evaluate_board(board, perspective)
        board.pop()

        if score > best_score + 1e-6:
            best_score = score
            best_moves = [move]
        elif abs(score - best_score) <= 1e-6:
            best_moves.append(move)

    return random.choice(best_moves) if best_moves else random.choice(list(board.legal_moves))


def record_move(board: chess.Board, move: chess.Move):
    san = board.san(move)
    board.push(move)
    st.session_state.move_history.append(san)


def attempt_player_move(move_text: str) -> bool:
    board = st.session_state.board
    player_turn = chess.WHITE if st.session_state.player_is_white else chess.BLACK

    if st.session_state.ai_enabled and board.turn != player_turn:
        st.warning("Please wait for the copilot to move.")
        return False

    move_text = move_text.strip()
    if not move_text:
        st.warning("Enter a move in SAN (`Nf3`) or UCI (`g1f3`).")
        return False

    move: Optional[chess.Move] = None
    try:
        move = board.parse_san(move_text)
    except ValueError:
        try:
            move = chess.Move.from_uci(move_text.lower())
            if move not in board.legal_moves:
                move = None
        except ValueError:
            move = None

    if move is None:
        st.error("Invalid move. Please try again.")
        return False

    san = board.san(move)
    board.push(move)
    st.session_state.move_history.append(san)
    st.session_state.status_message = f"Player played {san}"
    st.session_state.move_entry = ""
    return True


def trigger_ai_move():
    board = st.session_state.board
    if board.is_game_over():
        return
    ai_turn = board.turn
    if st.session_state.ai_enabled and ai_turn != (chess.WHITE if st.session_state.player_is_white else chess.BLACK):
        ai_move = choose_ai_move(board)
        san = board.san(ai_move)
        board.push(ai_move)
        st.session_state.move_history.append(san)
        st.session_state.status_message = f"Copilot played {san}"


def handle_square_click(square_name: str):
    board = st.session_state.board
    player_color = chess.WHITE if st.session_state.player_is_white else chess.BLACK
    allowed_color = player_color if st.session_state.ai_enabled else board.turn

    if st.session_state.ai_enabled and board.turn != player_color:
        st.warning("Copilot is still thinking. Please wait.")
        return

    selected = st.session_state.selected_square
    if selected is None:
        square = chess.parse_square(square_name)
        piece = board.piece_at(square)
        if piece is None or piece.color != allowed_color:
            st.info("Select one of your own pieces to move.")
            return
        st.session_state.selected_square = square_name
        st.session_state.status_message = f"Selected {square_name.upper()}."
        return

    if square_name == selected:
        st.session_state.selected_square = None
        st.session_state.status_message = "Selection cleared."
        return

    candidate_moves = [
        move
        for move in board.legal_moves
        if chess.square_name(move.from_square) == selected and chess.square_name(move.to_square) == square_name
    ]

    if not candidate_moves:
        st.warning("Illegal move. Try selecting a different destination.")
        st.session_state.selected_square = None
        return

    suffix = ""
    if any(move.promotion for move in candidate_moves):
        choice = st.session_state.get("promotion_choice", "Queen").lower()
        suffix = PROMOTION_LETTER_MAP.get(choice, "q")

    move_input = f"{selected}{square_name}{suffix}"
    if attempt_player_move(move_input):
        st.session_state.selected_square = None
        if st.session_state.ai_enabled:
            trigger_ai_move()


def display_status():
    board = st.session_state.board
    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        st.success(f"Checkmate! {winner} wins.")
    elif board.is_stalemate():
        st.info("Stalemate reached.")
    elif board.is_insufficient_material():
        st.info("Draw by insufficient material.")
    elif board.is_seventyfive_moves():
        st.info("Draw by 75-move rule.")
    elif board.is_fivefold_repetition():
        st.info("Draw by fivefold repetition.")
    else:
        st.write(st.session_state.status_message)


# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Streamlit Chess", layout="wide")
    init_state()

    st.title("♟️ Streamlit Chess Arena")
    st.caption("Play chess against a lightweight copilot or pass-and-play with a teammate.")

    with st.sidebar:
        st.header("Game controls")
        ai_toggle = st.checkbox("Play against copilot", value=st.session_state.ai_enabled)
        if ai_toggle != st.session_state.ai_enabled:
            st.session_state.ai_enabled = ai_toggle

        color_choice = st.radio(
            "Choose your pieces",
            options=["White", "Black"],
            index=0 if st.session_state.player_is_white else 1,
        )

        if color_choice != ("White" if st.session_state.player_is_white else "Black"):
            reset_game(color_choice)

        if st.button("Start new game", use_container_width=True):
            reset_game(color_choice)

        st.markdown(
            """
            **Tips**
            - Accepts SAN (`Bb5+`) or UCI (`b1c3`) inputs.
            - Toggle copilot off for local two-player games.
            - Orientation flips automatically based on your color.
            """
        )

    render_board()
    display_status()

    board = st.session_state.board
    player_turn = chess.WHITE if st.session_state.player_is_white else chess.BLACK

    if st.session_state.ai_enabled and board.turn != player_turn:
        st.info("Copilot is thinking... please wait.")

    st.selectbox(
        "Promotion choice (used when a pawn reaches the back rank)",
        options=["Queen", "Rook", "Bishop", "Knight"],
        key="promotion_choice",
    )

    helper_col, clear_col = st.columns([3, 1])
    with helper_col:
        selected = st.session_state.selected_square or "None"
        st.caption(f"Selected square: **{selected.upper() if selected != 'None' else 'None'}**")
    with clear_col:
        if st.button("Clear selection"):
            st.session_state.selected_square = None

    render_click_grid()

    with st.expander("Prefer typing a move?"):
        manual_move = st.text_input("Enter SAN or UCI move", key="manual_move")
        if st.button("Submit typed move", key="manual_submit"):
            if attempt_player_move(manual_move):
                st.session_state.selected_square = None
                if st.session_state.ai_enabled:
                    trigger_ai_move()

    st.subheader("Move history")
    show_move_history()


if __name__ == "__main__":
    main()
