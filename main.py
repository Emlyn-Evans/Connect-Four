import sys
from state_class import Board, State, Node


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
    state = State(board_str)

    print(state.board)
    print(state.board.get_filled_cols())

    state.compute_evaluation()
    state.print_evaluation()

    return


def generate_children():

    board_str = "yryrrry,.rryyrr,.yyyrr.,.ryy.y.,...r...,......."
    max_depth = 5
    last_move = "X"

    state = State(board_str)
    head = Node(state)
    head.last_move = last_move

    print(head.state.board)
    head.state.compute_evaluation()
    head.state.print_evaluation()

    # Creating children
    head.generate_children()

    print("Original")
    print(head.state.board)
    head.state.print_evaluation()

    for i in range(len(head.children)):

        print(f"Child: {i}")
        print(head.children[i].state.board)
        print(head.children[i].state.print_evaluation())
        print("\n")


def recursively_generate_children(node, depth, max_depth):

    if depth == max_depth:

        return

    node.generate_children()

    for i in range(len(node.children)):

        recursively_generate_children(node.children[i], depth + 1, max_depth)


def dfs_print(node, depth, max_depth):

    if depth == max_depth:

        print(f"Current Node: {node.name}")
        print(node.state.board)

        return

    for i in range(len(node.children)):

        dfs_print(node.children[i], depth + 1, max_depth)

    print(f"Current Node: {node.name}")
    print(node.state.board)

    return


def set_up_state():

    # Inputs
    # board_str = "yryrrry,.rryyrr,.yyyrr.,.ryy.y.,...r...,......."
    board_str = ".......,.......,.......,.......,.......,......."
    max_depth = 4
    last_move = "X"

    # Initialise
    state = State(board_str)
    head = Node(state, ".")
    head.last_move = last_move

    recursively_generate_children(head, 0, max_depth)

    dfs_print(head, 0, max_depth)


# create_state()
# example_evaluation()
# generate_children()
set_up_state()
