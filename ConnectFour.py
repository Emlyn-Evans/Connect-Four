import sys
import time

from classes import Board, Node, Trans_Table, Move_Sorter


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
        self.trans_table = Trans_Table(8388593)
        self.move_sorter = Move_Sorter()

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
        print(f"Opt path: {self.root.opt_string}")

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

        potential_map = self.board.bit_potential_map()

        # If opponent wins automatically on their next turn
        if potential_map == 0:

            self.board.n_terminal += 1

            return -self.board.get_utility()

        # If there have been 40 moves played and we can't win in the next two,
        # its a draw
        if self.board.moves_board >= (self.board.rows * self.board.cols) - 2:

            return 0

        # Lower bound the alpha as opponent cannot win next move by design
        min_value = -int(
            (self.board.rows * self.board.cols - 2 - self.board.moves_board) / 2
        )

        if alpha < min_value:

            alpha = min_value

            if alpha >= beta:

                print(f"Pruning out of loop for alpha...")

                return alpha

        # Upper bound the beta as we cannot win next move by design
        max_value = int(
            (self.board.rows * self.board.cols - 1 - self.board.moves_board) / 2
        )

        if beta > max_value:

            beta = max_value

            if alpha >= beta:

                print(f"Pruning out of loop for beta...")

                return beta

        # Transposition Table entry handling
        ret = self.trans_table.get_value(self.board.get_key())

        if ret is not None:

            # If we have a lower bound on the alpha
            if ret > self.board.max_utility - self.board.min_utility + 1:

                min_value = (
                    ret + (2 * self.board.min_utility) - self.board.max_utility - 2
                )

                if alpha < min_value:

                    alpha = min_value

                    if alpha >= beta:

                        return alpha

            # If we have an upper bound on the beta
            else:

                max_value = ret + self.board.min_utility - 1

                if beta > max_value:

                    beta = max_value

                    if alpha >= beta:

                        return beta

        # We only need to iterate over the potential_map
        # Sort potential moves
        self.move_sorter.reset()
        self.move_sorter.compute_move_order(potential_map, self.board)
        col = self.move_sorter.get_next_move()

        # print(f"Node: {node.name} Move Sorter: {self.move_sorter.cols}")

        while col is not None:

            # print(f"Adding child with col {col}")
            # time.sleep(0.1)

            # Make child with col
            self.board.add_move(col)
            child = node.add_child(self.board, col)

            print(f"Checking out: {child.name}")
            value = -self.alpha_beta_negamax(child, -beta, -alpha)

            if value > 0:

                if node.player == "X":

                    print(
                        f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for X found"
                    )

                else:

                    print(
                        f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for O found"
                    )

            elif value < 0:

                if node.player == "X":

                    print(
                        f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for O found"
                    )

                else:

                    print(
                        f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for X found"
                    )

            else:

                print(f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Draw")

            self.board.remove_move(col)

            # print(f" -- Alpha: {alpha} : Beta: {beta} : Value: {value}")

            # Cutoff time
            # if time.time() - self.start_time > self.cutoff_time:

            #     print("TIMEOUT")

            #     if value > alpha:

            #         alpha = value
            #         node.value = value
            #         node.opt_child = node.n_children
            #         node.opt_col = col

            #     return alpha

            # Update alpha and beta values
            if value >= beta:

                # Add lower bound to transposition table
                self.trans_table.add(
                    self.board.get_key(),
                    value + self.board.max_utility - (2 * self.board.min_utility) + 2,
                )
                node.value = value
                node.opt_child = node.n_children
                node.opt_col = col
                node.opt_string = child.opt_string + str(col)

                print(f"Pruning in loop...")

                return value

            if value > alpha:

                alpha = value
                node.value = value
                node.opt_child = node.n_children
                node.opt_col = col
                node.opt_string = child.opt_string + str(col)

            # Get next move (if there is one)
            col = self.move_sorter.get_next_move()

        # Add upper bound to position to transposition table
        self.trans_table.add(
            self.board.get_key(),
            (alpha - self.board.min_utility + 1),
        )

        return alpha


four_eyes = Four_Eyes(sys.argv[1], sys.argv[2])
