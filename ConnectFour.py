import sys

from classes import Board


def init(board_str, turn):

    if turn == "red":

        move = "X"

    else:

        move = "O"

    board = Board()
    board.create_board_from_str(board_str)

    print(f"X Bits: {board.x_bits} : Number: {board.x_num}")
    print(f"O Bits: {board.o_bits} : Number: {board.o_num}")

    print(board)

    return


init(sys.argv[1], sys.argv[2])