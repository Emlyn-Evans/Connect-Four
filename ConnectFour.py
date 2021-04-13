import sys
import time

from classes import Board, Node, Trans_Table


class Four_Eyes:
    def __init__(self, board_str, turn):

        self.start_time = time.time()
        self.cutoff_time = 0.8

        if turn == "red":

            move = "X"

        else:

            move = "O"

        self.board = Board(move)
        self.board.create_board_from_str(board_str)
        self.root = Node(".", move, 0)
        self.root.compute_utility(self.board)
        self.trans_table = Trans_Table(8388593)

        print(self.board)

        self.solve()

        return

    def solve(self):

        # Check if we can win in the next move
        win_col = self.board.bit_winning_col()

        if win_col is not None:

            self.root.opt_col = win_col
            return

        minimum = -int((self.board.rows * self.board.cols - self.board.moves_board) / 2)
        maximum = int(
            (self.board.rows * self.board.cols + 1 - self.board.moves_board) / 2
        )

        # Iterative deepining search method to restrain possible alpha-beta
        # values
        while minimum < maximum:

            # print(f"New Iteration: Min: {minimum} : Max: {maximum}")

            medium = minimum + int((maximum - minimum) / 2)

            if medium <= 0 and int(minimum / 2) < medium:

                medium = int(minimum / 2)

            elif medium >= 0 and int(maximum / 2) > medium:

                medium = int(maximum / 2)

            ret = self.alpha_beta_negamax(self.root, medium, medium + 1)

            if ret <= medium:

                maximum = ret

            else:

                minimum = ret

            if time.time() - self.start_time > self.cutoff_time:

                break

        # print(f"Minimum: {minimum}")

        print(
            f"\nNodes analysed: {self.board.n_nodes} : Terminal nodes found: {self.board.n_terminal} : Max depth: {self.board.n_depth}"
        )
        print(f"{self.root}\n")
        print(f"Last Node analysed: {self.board.last_node}")
        print(f"TT hits: {self.trans_table.hits} | misses: {self.trans_table.misses}")

    def alpha_beta_negamax(self, node, alpha, beta):

        # print(f"Alpha: {alpha} : Beta: {beta}")
        # print(f"Depth: {node.depth} | Name: {node.name}")
        # time.sleep(0.01)

        self.board.n_nodes += 1
        self.board.last_node = node.name

        if self.trans_table.table.__sizeof__() > 70000000:

            print("TT TOO BIG")

        if node.depth > self.board.n_depth:

            self.board.n_depth = node.depth

        # If it is a terminal node, return the utility value
        if node.compute_utility(self.board) is not None:

            self.board.n_terminal += 1

            return node.utility

        stop_opponent = self.board.bit_stop_opponent_col()

        # Opponent wins automatically next turn
        if stop_opponent == -2:

            return -self.board.get_score()

        max_value = int(
            (self.board.rows * self.board.cols - 1 - self.board.moves_board) / 2
        )

        # Transtable check here
        ret = self.trans_table.get_value(self.board.get_key())

        if ret is not None:

            max_value = ret - (int((self.board.rows * self.board.cols) / 2) + 3) - 1

        if beta > max_value:

            beta = max_value

            # Alpha beta
            if alpha >= beta:

                return beta

        # Iterate through all possible children, considering cutoffs
        for i in range(self.board.cols):

            if stop_opponent >= 0:

                col = stop_opponent
                i = self.board.cols

            else:

                col = self.board.order[i]

            if self.board.check_filled(col) == 0:

                self.board.add_move(col)
                child = node.add_child(self.board, col)
                value = -self.alpha_beta_negamax(child, -beta, -alpha)
                self.board.remove_move(col)

                # print(f" -- Alpha: {alpha} : Beta: {beta} : Value: {value}")

                # Cutoff time
                if time.time() - self.start_time > self.cutoff_time:

                    if value > alpha:

                        alpha = value
                        node.value = value
                        node.opt_child = node.n_children
                        node.opt_col = col

                    return alpha

                # Update alpha and beta values
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

        # Add position to transposition table
        self.trans_table.add(
            self.board.get_key(),
            (alpha + (int((self.board.rows * self.board.cols) / 2) + 3) + 1),
        )

        return alpha


four_eyes = Four_Eyes(sys.argv[1], sys.argv[2])