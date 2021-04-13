import sys
import time

from classes import Board, Node, Trans_Table


class Four_Eyes:
    def __init__(self, board_str, turn):

        start_time = time.time()

        if turn == "red":

            move = "X"

        else:

            move = "O"

        self.board = Board(move)
        self.board.create_board_from_str(board_str)
        # print(
        #     f"X bits: {self.board.get_bin(self.board.get_player_pos('X'))} : Number: {self.board.get_player_pos('X')}"
        # )
        # print(
        #     f"O bits: {self.board.get_bin(self.board.get_player_pos('O'))} : Number: {self.board.get_player_pos('O')}"
        # )

        print(self.board)
        # print(f"Player turn: {self.board.player}")
        # print(f"Win for X: {self.board.check_win('X')}")
        # print(f"Win for O: {self.board.check_win('O')}")
        # print(
        #     f"Board moves: {self.board.moves_board} : Player moves: {self.board.moves_player}"
        # )

        self.root = Node(".", move, 0)
        self.root.compute_utility(self.board)
        self.trans_table = Trans_Table(8388593)

        self.solve(start_time)

        # test_move(board)

        return

    def solve(self, start_time):

        minimum = -int((self.board.rows * self.board.cols - self.board.moves_board) / 2)
        maximum = int(
            (self.board.rows * self.board.cols + 1 - self.board.moves_board) / 2
        )

        while minimum < maximum:

            # print(f"New Iteration: Min: {minimum} : Max: {maximum}")

            medium = minimum + int((maximum - minimum) / 2)

            if medium <= 0 and int(minimum / 2) < medium:

                medium = int(minimum / 2)

            elif medium >= 0 and int(maximum / 2) > medium:

                medium = int(maximum / 2)

            ret = self.alpha_beta_negamax(self.root, medium, medium + 1, start_time)

            if ret <= medium:

                maximum = ret

            else:

                minimum = ret

        # print(f"Minimum: {minimum}")

        print(
            f"\nNodes analysed: {self.board.n_nodes} : Terminal nodes found: {self.board.n_terminal} : Max depth: {self.board.n_depth}"
        )
        print(f"{self.root}\n")

        print(f"TT hits: {self.trans_table.hits} | misses: {self.trans_table.misses}")

    def alpha_beta_negamax(self, node, alpha, beta, start_time):

        # print(f"Alpha: {alpha} : Beta: {beta}")

        # if len(node.name) > 2 and node.name[1] != "3":
        print(f"Depth: {node.depth} | Name: {node.name}")
        time.sleep(0.01)

        self.board.n_nodes += 1
        # print(f"Nodes: {self.board.n_nodes}")
        if self.trans_table.table.__sizeof__() > 70000000:

            print("TT TOO BIG")

        if node.depth > self.board.n_depth:

            self.board.n_depth = node.depth

        if node.compute_utility(self.board) is not None:

            # print(f"\nFound terminal node at depth {node.depth}")
            # print(node)
            # print(board)

            # print(f"Found terminal node, value: {node.utility}")
            self.board.n_terminal += 1
            # print(f"Terminal Nodes: {self.board.n_terminal}")

            return node.utility

        win_col = self.board.bit_winning_col()

        if win_col is not None:

            print("Shortcut found")

            # Play winning move
            self.board.n_terminal += 1
            node.opt_col = win_col

            child = Node(
                node.name + str(win_col),
                self.board.get_other_player(),
                node.depth + 1,
                node,
            )
            node.children.append(child)
            node.n_children += 1
            child.utility = (self.board.moves_board - self.board.moves_player) - 22

            return -child.utility

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

        for i in range(self.board.cols):

            col = self.board.order[i]

            if self.board.check_filled(col) == 0:

                self.board.add_move(col)
                child = node.add_child(self.board, col)
                value = -self.alpha_beta_negamax(child, -beta, -alpha, start_time)
                self.board.remove_move(col)

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
                # if time.time() - start_time > 0.8:

                #     return alpha

        self.trans_table.add(
            self.board.get_key(),
            (alpha + (int((self.board.rows * self.board.cols) / 2) + 3) + 1),
        )

        return alpha


four_eyes = Four_Eyes(sys.argv[1], sys.argv[2])