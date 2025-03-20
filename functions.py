import chess
import chess.svg


def generate_move_comment(evaluation):
    comment = ""
    if evaluation["type"] == "cp":
        if evaluation["value"] > 100:
            comment = "Отличный ход! Он значительно улучшает вашу позицию."
        elif evaluation["value"] > 0:
            comment = "Хороший ход, но не решающий."
        elif evaluation["value"] < -100:
            comment = "Плохой ход, он серьезно ухудшает вашу позицию."
        elif evaluation["value"] < 0:
            comment = "Ошибка! Этот ход ослабляет вашу позицию."
        else:
            comment = "Нейтральный ход, позиция остаётся неизменной."
    elif evaluation["type"] == "mate":
        comment = f"**Внимание! Возможен мат!**"

    return comment


def highlights(board, best_move, highlight_cells=None):
    board_svg = chess.svg.board(board=board)

    if best_move:
        move_from = best_move[:2]
        move_to = best_move[2:]

        from_square = chess.parse_square(move_from)
        to_square = chess.parse_square(move_to)

        board_svg = chess.svg.board(board=board, arrows=[(from_square, to_square)])

    return board_svg