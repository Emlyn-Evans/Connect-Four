# A file to house the minimax algorithm logic

from state_class import Node, State, Board


def init():

    # Initialise

    board_str = "..yrr..,..ry...,...y...,.......,.......,......."
    max_depth = 4
    last_move = "O"

    state = State(board_str)
    head = Node(state, ".")
    head.last_move = last_move

    return head


def test_1(head):

    print(head.state.board)
    head.state.print_evaluation()

    return


test_1(init())