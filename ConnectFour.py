import sys

from classes import Board


def init(board_str, turn):

    if turn == "red":

        move = "X"

    else:

        move = "O"

    board = Board(move)
    board.create_board_from_str(board_str)

    print(
        f"X bits: {board.get_bin(board.get_player_pos('X'))} : Number: {board.get_player_pos('X')}"
    )
    print(
        f"O bits: {board.get_bin(board.get_player_pos('O'))} : Number: {board.get_player_pos('O')}"
    )

    print(board)
    print(f"Player turn: {board.player}")
    print(f"Win for X: {board.check_win('X')}")
    print(f"Win for O: {board.check_win('O')}")

    col = 5
    print(f"Adding move to col {col}")

    board.add_move(col)

    print(board)
    print(f"Player turn: {board.player}")

    print(f"Removing move")

    board.remove_move(col)

    print(board)
    print(f"Player turn: {board.player}")

    return


init(sys.argv[1], sys.argv[2])