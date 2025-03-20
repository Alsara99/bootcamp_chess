import streamlit as st
import chess.pgn
from stockfish import Stockfish
from io import StringIO
from functions import *

st.title("♟️Шахматный анализатор by Singularity Hub")
mode = st.radio("Выберите способ загрузки:", ["PGN-файл", "FEN-ввод"])

stockfish_path = "stockfish/stockfish.exe"
stockfish = Stockfish(path=stockfish_path)
stockfish.set_depth(18)

#PGN-файл
if mode == "PGN-файл":
    uploaded_file = st.file_uploader("Загрузите PGN-файл", type=["pgn"])

    if uploaded_file:
        pgn_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
        game = chess.pgn.read_game(pgn_data)

        st.subheader("🔎 Информация о партии")
        st.write(f"**♘Белые:** {game.headers['White']}")
        st.write(f"**♟️Чёрные:** {game.headers['Black']}")
        st.write(f"**🏁Результат:** {game.headers['Result']}")

        # Создаём доску
        board = game.board()
        moves = list(game.mainline_moves())
        moves.append('-')

        if "move_index" not in st.session_state:
            st.session_state.move_index = 0
            st.session_state.last_move = '-'

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏪ Назад") and st.session_state.move_index > 0:
                st.session_state.move_index -= 1
        with col2:
            if st.button("⏩ Вперёд") and st.session_state.move_index < len(moves)-1:
                st.session_state.move_index += 1

        for move in moves[:st.session_state.move_index]:

            board.push(move)

        fen = board.fen()

        stockfish.set_fen_position(fen)
        best_move = stockfish.get_best_move()
        evaluation = stockfish.get_evaluation()


        move = moves[st.session_state.move_index-1]

        comment = generate_move_comment(evaluation)


        st.subheader("🔍 Анализ позиции")
        st.write(f"**🔄Текущий ход:** {move}")
        st.write(f"**🔥Лучший ход:** {best_move if best_move else '**Нет доступных ходов**'}")
        st.write(f"**💬Комментарий**: {comment}")

        if evaluation["type"] == "cp":
            st.write(f"**📊Оценка позиции:** {evaluation['value'] / 100:.2f}")
        elif evaluation["type"] == "mate":
            num = str(evaluation['value'])[-1]
            if evaluation['value'] != 0:
                if 0 < int(num) < 2:
                    st.write(f"**Мат через {evaluation['value']} ход!🏁♟️🔥**")
                elif 0 < int(num) < 5 :
                    st.write(f"**Мат через {evaluation['value']} хода!🏁♟️🔥**")
                else:
                    st.write(f"**Мат через {evaluation['value']} ходов!🏁♟️🔥**")
            else:
                st.write("**Мат!🏆♟️💥**")

        board_svg = highlights(board, best_move, [str(move)[:2], str(move)[2:]])
        st.markdown(f'<div style="text-align: center;">{board_svg}</div>', unsafe_allow_html=True)

#FEN-ВВОД
else:
    fen = st.text_input("Введите FEN:", "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2")

    board = chess.Board(fen)

    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    evaluation = stockfish.get_evaluation()

    st.subheader("🔍 Анализ позиции")
    st.write(f"**🔥Лучший ход:** {best_move if best_move else 'Нет доступных ходов'}")

    if evaluation["type"] == "cp":
        st.write(f"**📊Оценка позиции:** {evaluation['value'] / 100:.2f}")
    elif evaluation["type"] == "mate":
        st.write(f"**Мат через {evaluation['value']} ходов!🏁♟️🔥**")

    board_svg = highlights(board, best_move)
    st.markdown(f'<div style="text-align: center;">{board_svg}</div>', unsafe_allow_html=True)