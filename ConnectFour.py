import sys
import time

from classes import Board, Node, Trans_Table, Move_Sorter, Book

"""
Tournament AI to play Connect Four.

Absolute credit goes to the guy that authored this blog:
- http://blog.gamesolver.org/solving-connect-four/01-introduction/

I followed this guide and implemented my own version based off most of the ideas
in the blog. I found his ideas interesting and useful and it was a lot of fun to
learn and understand them so I could do them myself. There were many times when
I tried to stray from the path outlined for originality purposes, but always
resorted to coming back as this blog outlined the easiest and most efficient
methods of implementation (but at least I realised why in the end).

Thanks also to:
- https://connect4.gamesolver.org/en

For allowing me to play my AI against it as a baseline for generating the book
moves.

Overall, I had a lot of fun doing this project and I'll be slightly pissed off
if the bot gets timed out due to initialising python and all it's overheads.

"""


class Four_Eyes:
    def __init__(self, board_str, turn, start_time):

        self.start_time = start_time
        self.cutoff_time = 0.75

        if turn == "red":

            move = "X"

        else:

            move = "O"

        self.board = Board(move)
        self.board.create_board_from_str(board_str)
        self.root = Node(".", move, 0)
        self.trans_table = Trans_Table(8388593)
        self.book = Book()
        self.book.read_oracle()
        self.book.fix_mistakes()

        # print(self.board)

        self.solve()

        return

    def solve(self):

        # Check if we can win in the next move
        win_col = self.board.bit_winning_col()

        if win_col is not None:

            self.root.opt_col = win_col

        # Check if the position is in book
        key = self.board.get_key()

        if key in self.book.oracle:

            self.root.opt_col = self.book.oracle[key]

        # Check if the symmetrical position is in the oracle
        sym_key = self.board.bit_symmetry_key()

        if sym_key in self.book.oracle:

            self.root.opt_col = 6 - self.book.oracle[sym_key]

        # If not, we need to search
        if self.root.opt_col is None:

            minimum = -int(
                (self.board.rows * self.board.cols - self.board.moves_board) / 2
            )
            maximum = int(
                (self.board.rows * self.board.cols + 1 - self.board.moves_board) / 2
            )

            # Iterative deepining search method to restrain possible alpha-beta
            # values by a middle value
            while minimum < maximum:

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

                # If we exceed the cutoff, quit the program and return the best
                # move so far
                if time.time() - self.start_time > self.cutoff_time:

                    break

        # print(
        #     f"\nNodes analysed: {self.board.n_nodes} : Terminal nodes found: {self.board.n_terminal} : Max depth: {self.board.n_depth}"
        # )
        # print(f"{self.root}\n")
        # print(f"Last Node analysed: {self.board.last_node}")
        # print(f"TT hits: {self.trans_table.hits} | misses: {self.trans_table.misses}")
        # print(f"Opt path: {self.root.opt_string}")

        if self.root.opt_col is None:

            time.sleep(2)

        else:

            print(f"{self.root.opt_col}")

        return

    def alpha_beta_negamax(self, node, alpha, beta):

        # print(f"Alpha: {alpha} : Beta: {beta}")
        # print(f"Depth: {node.depth} | Name: {node.name}")
        # time.sleep(0.01)

        self.board.n_nodes += 1
        self.board.last_node = node.name

        # if self.trans_table.table.__sizeof__() > 70000000:

        #     print("TT TOO BIG")

        # if node.depth > self.board.n_depth:

        #     self.board.n_depth = node.depth

        # Generate a map of all potential positions to play (possible and safe)
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

                # print(f"Pruning out of loop for alpha...")

                return alpha

        # Upper bound the beta as we cannot win next move by design
        max_value = int(
            (self.board.rows * self.board.cols - 1 - self.board.moves_board) / 2
        )

        if beta > max_value:

            beta = max_value

            if alpha >= beta:

                # print(f"Pruning out of loop for beta...")

                return beta

        # Transposition Table entry handling
        ret = self.trans_table.get_value(self.board.get_key())

        if ret is None:

            ret = self.trans_table.get_value(self.board.bit_symmetry_key())

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
        # Sort potential moves by evaluation function
        move_sorter = Move_Sorter()
        move_sorter.compute_move_order(potential_map, self.board)
        col = move_sorter.get_next_move()

        # print(f"Node: {node.name} Move Sorter: {self.move_sorter.cols}")

        while col is not None:

            # print(f"Adding child with col {col}")
            # time.sleep(0.1)

            # Make child with col
            self.board.add_move(col)
            child = node.add_child(self.board, col)

            # print(f"Checking out: {child.name}")
            value = -self.alpha_beta_negamax(child, -beta, -alpha)

            self.board.remove_move(col)

            # if value > 0:

            #     if node.player == "X":

            #         print(
            #             f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for X found"
            #         )

            #     else:

            #         print(
            #             f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for O found"
            #         )

            # elif value < 0:

            #     if node.player == "X":

            #         print(
            #             f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for O found"
            #         )

            #     else:

            #         print(
            #             f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Win for X found"
            #         )

            # else:

            #     print(f"Return val: {value} Alpha: {alpha} : Beta: {beta} : Draw")

            # print(f" -- Alpha: {alpha} : Beta: {beta} : Value: {value}")

            # Cutoff time
            if time.time() - self.start_time > self.cutoff_time:

                # print("TIMEOUT")

                if value > alpha:

                    alpha = value

                    node.value = value
                    node.opt_child = node.n_children
                    node.opt_col = col
                    node.opt_string = str(node.opt_col) + child.opt_string

                if node.opt_col is None:

                    node.opt_child = node.n_children
                    node.opt_col = col
                    node.opt_string = str(node.opt_col) + child.opt_string

                return alpha

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
                node.opt_string = str(node.opt_col) + child.opt_string

                # print(f"Pruning in loop...")

                return value

            # Store best child so far
            if value > alpha:

                alpha = value
                node.value = value
                node.opt_child = node.n_children
                node.opt_col = col
                node.opt_string = str(node.opt_col) + child.opt_string

            # Get next move (if there is one)
            col = move_sorter.get_next_move()

        node.opt_string = str(node.opt_col) + child.opt_string

        # Add upper bound to position to transposition table
        self.trans_table.add(
            self.board.get_key(),
            (alpha - self.board.min_utility + 1),
        )

        return alpha


def oracle_builder():

    book = Book()
    book.read_oracle()
    book.fix_mistakes()

    n_moves = 3

    # Build for X
    # Here we can start from the baseline
    print("Run 1")
    book.set_board("X", ".......,.......,.......,.......,.......,.......")
    book.build_oracle(n_moves)

    # Build for O
    # Here we have to run it 7 times for each of the starting X moves

    print("Run 2")
    book.set_board("O", "r......,.......,.......,.......,.......,.......")
    book.build_oracle(n_moves)
    print("Run 3")
    book.set_board("O", ".r.....,.......,.......,.......,.......,.......")
    book.build_oracle(n_moves)
    print("Run 4")
    book.set_board("O", "..r....,.......,.......,.......,.......,.......")
    book.build_oracle(n_moves)
    print("Run 5")
    book.set_board("O", "...r...,.......,.......,.......,.......,.......")
    book.build_oracle(n_moves)

    # Write
    book.write_oracle("output.txt")


start_time = time.time()
Four_Eyes(sys.argv[1], sys.argv[2], start_time)

# print(f"Program ran for {time.time() - start_time}")
# oracle_builder()
