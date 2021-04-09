import sys
from state_class import Board, State


def print_arguments():

    board_str = sys.argv[1]
    player_turn = sys.argv[2]
    algorithm = sys.argv[3]
    max_depth = int(sys.argv[4])

    print(f"Board: {board_str}")
    print(f"Player turn: {player_turn}")
    print(f"Algorithm type: {algorithm}")
    print(f"Max depth of search: {max_depth}")

    return


def get_board_str():

    return sys.argv[1]


def create_state():

    board_str = get_board_str()
    state = State(board_str)

    print(state.board)
    print(state.board.get_filled_cols())

    adjust_state(state)

    return


def adjust_state(state):

    # Adjust board:
    state.board.add_move(0, "X")
    state.board.add_move(1, "X")
    state.board.add_move(2, "X")
    state.board.add_move(3, "X")
    state.board.add_move(4, "X")
    state.board.add_move(5, "X")
    state.board.add_move(6, "X")
    print(state.board)
    print(state.board.get_filled_cols())

    state.board.add_move(2, "O")
    state.board.add_move(2, "O")
    print(state.board)
    print(state.board.get_filled_cols())

    return


def example_evaluation():

    board_str = "..yyrrr,..ryryr,....y..,.......,.......,......."
    test_2 = "ryryyyr,.yyrryy,.rrryy.,.yrrrr.,...y...,......."
    test_2 = "yryrrry,.rryyrr,.yyyrr.,.ryyyy.,...r...,......."
    state = State(test_2)

    print(state.board)
    print(state.board.get_filled_cols())

    state.compute_evaluation()
    state.print_evaluation()

    return


# create_state()
example_evaluation()
