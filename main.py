import sys
from state_class import Board, State, Node


# def print_arguments():

#     board_str = sys.argv[1]
#     player_turn = sys.argv[2]
#     algorithm = sys.argv[3]
#     max_depth = int(sys.argv[4])

#     print(f"Board: {board_str}")
#     print(f"Player turn: {player_turn}")
#     print(f"Algorithm type: {algorithm}")
#     print(f"Max depth of search: {max_depth}")

#     return


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


def compute_minimax(node, depth, max_depth):

    # if node.state.utility != 0:

    #     return node.state.utility

    if depth == max_depth:

        node.minimax = node.state.evaluation

        print(f"Node: {node.name} has minimax: {node.minimax}")

        return node.minimax

    if node.last_move == "O":

        alpha = None
        alpha_index = None

        for i in range(len(node.children)):

            ret = compute_minimax(node.children[i], depth + 1, max_depth)

            # if depth == 0:
            #     print(
            #         f"MAX: {node.children[i].name}: {ret} for child {i} in depth {depth}"
            #     )

            if alpha is None:

                alpha = ret
                alpha_index = i

            elif ret > alpha:

                alpha = ret
                alpha_index = i

        # print(f"Taking max: {alpha} in depth {depth}")
        node.minimax = alpha
        node.minimax_index = alpha_index
        print(
            f"Taking MAX: Node: {node.name} has minimax: {node.minimax} from child {node.minimax_index}"
        )

    else:

        beta = None
        beta_index = None

        for i in range(len(node.children)):

            ret = compute_minimax(node.children[i], depth + 1, max_depth)

            # if depth == 1:
            # print(
            #     f"MIN: {node.children[i].name}: {ret} for child {i} in depth {depth}"
            # )

            if ret is None:
                print(f"Something wrong at node: {node.name} child: {i}")

            if beta is None:

                beta = ret
                beta_index = i

            elif ret < beta:

                beta = ret
                beta_index = i

        # print(f"Taking min: {beta} in depth {depth}")

        node.minimax = beta
        node.minimax_index = beta_index

        print(
            f"Taking MIN: Node: {node.name} has minimax: {node.minimax} from child {node.minimax_index}"
        )

    return node.minimax


def set_up_state():

    # Inputs
    board_str = "yryrrry,.rry.r.,.yyy.r.,.ryy.y.,...r...,......."
    # board_str = ".yrry..,..ryr..,..yry..,.......,.......,......."
    # board_str = ".......,.......,.......,.......,.......,......."
    max_depth = 4
    last_move = "O"

    # Initialise
    state = State(board_str)
    head = Node(state, ".")
    head.last_move = last_move

    recursively_generate_children(head, 0, max_depth)

    compute_minimax(head, 0, max_depth)

    print("\n\n----------------\n")

    current_node = head

    while len(current_node.children) != 0:

        print(
            f"Current Node: {current_node.name} : Minimax: {current_node.minimax} : Next Child: {current_node.minimax_index}"
        )
        print(current_node.state.board)
        print(current_node.state.print_evaluation())

        current_node = current_node.children[current_node.minimax_index]

    print(
        f"Current Node: {current_node.name} : Minimax: {current_node.minimax} : Next Child: {current_node.minimax_index}"
    )
    print(current_node.state.board)
    print(current_node.state.print_evaluation())

    # dfs_print(head, 0, max_depth)


# create_state()
# example_evaluation()
# generate_children()
set_up_state()
