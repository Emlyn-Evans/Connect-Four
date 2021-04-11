from classes import State, Board

# function alphabeta(node, depth, α, β, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
#             α := max(α, value)
#             if α ≥ β then
#                 break (* β cutoff *)
#         return value
#     else
#         value := +∞
#         for each child of node do
#             value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
#             β := min(β, value)
#             if β ≤ α then
#                 break (* α cutoff *)
#         return value


def alpha_beta(board, state, depth, max_depth, alpha, beta):

    board.n_states += 1

    # Terminal test:
    if state.utility != 0:

        return state.utility

    if depth == max_depth:

        return state.evaluation

    move = None

    # Maximising
    if state.last_move == "O":

        move = "X"

    else:

        move = "O"

    for i in range(len(board.filled_cols)):

        if board.filled_cols[i] < 6:

            # Create new child and recurse
            board.add_move(i, move)
            child = state.add_child(board, i)
            value = alpha_beta(board, child, depth + 1, max_depth, alpha, beta)
            board.remove_move(i)

            if state.value is None:

                state.value = value
                state.opt_child = i

            # Maximising
            if move == "X":

                if value > state.value:

                    state.value = value
                    state.opt_child = i

                # Beta Pruning: update alpha for local states in tree
                if state.value > alpha:

                    alpha = state.value

                if alpha >= beta:

                    break

            # Minimising
            else:

                if value < state.value:

                    state.value = value
                    state.opt_child = i

                # Alpha Pruning: update beta for local states in tree
                if state.value < beta:

                    beta = state.value

                if beta <= alpha:

                    break

        else:

            state.value = state.evaluation

    return state.value
