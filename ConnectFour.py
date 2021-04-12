import sys
import time

from classes import Board, Node


def init(board_str, turn):

    start_time = time.time()

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
    print(f"Board moves: {board.moves_board} : Player moves: {board.moves_player}")

    root = Node(".", move, 0)
    root.compute_utility(board)

    # test_move(board)
    alpha_beta_negamax(board, root, -22, 22, start_time)

    print(
        f"\nNodes analysed: {board.n_nodes} : Terminal nodes found: {board.n_terminal} : Max depth: {board.n_depth}"
    )
    print(f"{root}\n")

    return


def alpha_beta_negamax(board, node, alpha, beta, start_time):

    # print(f"Alpha: {alpha} : Beta: {beta}")

    board.n_nodes += 1
    print(f"Nodes: {board.n_nodes}")

    if node.depth > board.n_depth:

        board.n_depth = node.depth

    if node.compute_utility(board) is not None:

        # print(f"\nFound terminal node at depth {node.depth}")
        # print(node)
        # print(board)

        # print(f"Found terminal node: {node.name}")
        board.n_terminal += 1
        print(f"Terminal Nodes: {board.n_terminal}")

        return node.utility

    max_value = 21

    if beta > max_value:

        beta = max_value

        # Alpha beta
        if alpha >= beta:

            return beta

    for i in range(board.cols):

        col = board.order[i]

        if board.check_filled(col) == 0:

            board.add_move(col)
            child = node.add_child(board, col)
            value = -alpha_beta_negamax(board, child, -beta, -alpha, start_time)
            board.remove_move(col)

            # print(f" -- Alpha: {alpha} : Beta: {beta} : Value: {value}")

            if value >= beta:

                node.value = value
                node.opt_child = node.n_children
                node.opt_col = col

                return value

            if value > alpha:

                alpha = value

                node.value = value
                node.opt_child = node.n_children
                node.opt_col = col

            # Cutoff time
            if time.time() - start_time > 0.8:

                return alpha

    return alpha


init(sys.argv[1], sys.argv[2])