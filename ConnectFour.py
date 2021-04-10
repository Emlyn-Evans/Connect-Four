# A file to house the minimax algorithm logic
import sys
from classes import Board, State


def tree_print(state):

    print(state)

    for i in state.children:

        tree_print(i)


def tree_search_print(board, root):

    current_state = root
    while current_state.opt_child is not None:

        print(board)
        print(current_state)

        col = current_state.opt_child
        current_state = current_state.children[current_state.opt_child]
        board.add_move(col, current_state.last_move)

    print(board)
    print(current_state)


def minimax_recursion(board, state, depth, max_depth):

    board.n_states += 1

    # Check goal state
    if state.utility != 0:

        state.value = state.utility
        return state.value

    # Check leaf
    if depth == max_depth:

        state.value = state.evaluation
        return state.value

    # Non-leaf and non-goal nodes take minimax

    move = None

    if state.last_move == "O":
        move = "X"

    else:
        move = "O"

    for i in range(len(board.filled_cols)):

        if board.filled_cols[i] < 6:

            board.add_move(i, move)
            child = state.add_child(board, i)
            value = minimax_recursion(board, child, depth + 1, max_depth)
            board.remove_move(i)

            if state.value is None:

                state.value = value
                state.opt_child = i

                if move == "X":

                    if state.value == 10000:

                        break

                else:

                    if state.value == -10000:

                        break

            else:

                # Maximising
                if move == "X":

                    if value > state.value:

                        state.value = value
                        state.opt_child = i

                        if state.value == 10000:

                            break

                # Minimising
                else:

                    if value < state.value:

                        state.value = value
                        state.opt_child = i

                        if state.value == -10000:

                            break

    if state.value is None:

        # All columns filled
        state.value = state.evaluation

    return state.value


def minimax_wrapper(board_str, turn, max_depth):

    if turn == "red":

        last_move = "O"

    else:

        last_move = "X"

    board = Board()
    board.create_board_from_str(board_str)
    root = State(".", last_move)
    root.compute_evaluation(board)

    minimax_recursion(board, root, 0, max_depth)

    # tree_search_print(board, root)
    # tree_print(root)

    print(root.opt_child)
    print(board.n_states)


def alpha_beta_recursion(board, state, depth, max_depth):

    board.n_states += 1

    # print(depth * "- " + f"Checking state: {state.name}")

    # Check goal state
    if state.utility != 0:

        # print(depth * "- " + f"Goal state: {state.utility}")

        state.value = state.utility
        return state.value

    # Check leaf
    if depth == max_depth:

        # print(depth * "- " + f"Leaf state: {state.evaluation}")

        state.value = state.evaluation
        return state.value

    # Non-leaf and non-goal nodes take minimax

    move = None

    if state.last_move == "O":
        move = "X"

    else:
        move = "O"

    # print(depth * "- " + "Generating children...")

    for i in range(len(board.filled_cols)):

        if board.filled_cols[i] < 6:

            board.add_move(i, move)
            child = state.add_child(board, i)

            # ##
            # old = child.evaluation
            # old_str = f"E: {child.evaluation} X: {child.score_X} O: {child.score_O}"

            # child.compute_evaluation(board)
            # new = child.evaluation

            # if old != new:

            #     print(f"MISMATCH EVAL: old: {old_str} new: {new}")
            #     print(state)
            #     print(child)
            #     print(board)

            # ##

            value = alpha_beta_recursion(board, child, depth + 1, max_depth)
            # print(depth * "- " + f"Value received from child {i}: {value}")
            board.remove_move(i)

            if state.value is None:

                state.value = value
                state.opt_child = i

                # print(depth * "-" + f"Setting {state.name} value to {value}")

                if move == "X":

                    if state.value == 10000:

                        break

                else:

                    if state.value == -10000:

                        break

            else:

                # Maximising
                if move == "X":

                    if value > state.value:

                        old_value = state.value
                        state.value = value
                        state.opt_child = i

                        # print(
                        #     depth * "- "
                        #     + f"Maximising {state.name} value from {old_value} to {value}"
                        # )

                        if state.value == 10000:

                            break

                # Minimising
                else:

                    if value < state.value:

                        old_value = state.value

                        state.value = value
                        state.opt_child = i

                        # print(
                        #     depth * "- "
                        #     + f"Minimising {state.name} value from {old_value} to {value}"
                        # )

                        if state.value == -10000:

                            break

            # Alpha beta pruning
            if state.parent is not None:

                if state.parent.value is not None:

                    # print(
                    #     depth * "- "
                    #     + f"Parent {state.parent.name} value: {state.parent.value}"
                    # )

                    if move == "X":

                        if state.value >= state.parent.value:

                            # print(
                            #     depth * "- "
                            #     + f"Beta pruning as {state.name} >= {state.parent.value}"
                            # )

                            break

                    else:

                        if state.value <= state.parent.value:

                            # print(
                            #     depth * "- "
                            #     + f"Alpha pruning as {state.value} <= {state.parent.value}"
                            # )

                            break

    if state.value is None:

        # All columns filled
        state.value = state.evaluation

    return state.value


def alpha_beta_wrapper(board_str, turn, max_depth):

    if turn == "red":

        last_move = "O"

    else:

        last_move = "X"

    board = Board()
    board.create_board_from_str(board_str)
    root = State(".", last_move)
    root.compute_evaluation(board)

    alpha_beta_recursion(board, root, 0, max_depth)

    # tree_print(root)
    # tree_search_print(board, root)

    print(root.opt_child)
    print(board.n_states)


def test_eval():

    board_str = "rryyrry,yrryry.,r.y.r..,y.y....,.......,......."
    board_str = "rryy.yy,rr...yy,.......,.......,.......,......."

    board = Board()
    board.create_board_from_str(board_str)

    state = State(".", "X")
    state.compute_evaluation(board)

    print(board)
    print(state)


if sys.argv[3] == "M":

    minimax_wrapper(sys.argv[1], sys.argv[2], int(sys.argv[4]))

elif sys.argv[3] == "A":

    alpha_beta_wrapper(sys.argv[1], sys.argv[2], int(sys.argv[4]))

else:

    test_eval()