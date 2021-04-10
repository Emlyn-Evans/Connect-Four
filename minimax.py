# A file to house the minimax algorithm logic

from classes import Board, State


def init():

    # Initialise

    board_str = "..yrr..,..ry...,...y...,.......,.......,......."
    max_depth = 4
    last_move = "O"

    board = Board()
    board.create_board_from_str(board_str)
    head = State(".", last_move)
    head.compute_evaluation(board)

    return head, board


def test_1(head, board):

    print(board)
    print(head)

    board.add_move(5, "X")
    child = head.add_child(board, 5)

    print(board)
    print(child)

    board.add_move(4, "X")
    child_2 = child.add_child(board, 4)

    print(board)
    print(child_2)

    board.add_move(4, "O")
    child_3 = child_2.add_child(board, 4)

    print(board)
    print(child_3)

    # Don;t call add child if state is goal state

    return


head, board = init()
test_1(head, board)