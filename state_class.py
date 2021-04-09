class Token:
    def __init__(self, char):

        self.char = char
        # self.row = row
        # self.col = col

        # r = 0, ur = 1, u = 2, ul = 3
        self.directions = [1, 1, 1, 1]

    def __str__(self):

        return self.token


class Board:
    def __init__(self, board_str):

        self.board = self.create_board(board_str)
        self.filled_cols = self.compute_filled_cols()

        return

    def create_board(self, board_str):

        board = []
        rows = board_str.split(",")

        for row_str in rows:

            row = []

            for char in row_str:

                token = None

                if char == "r":

                    token = Token("X")

                elif char == "y":

                    token = Token("O")

                else:

                    token = Token(".")

                row.append(token)

            board.append(row)

        return board

    def compute_filled_cols(self):

        cols = [0, 0, 0, 0, 0, 0, 0]

        for row in self.board:

            for col in range(len(row)):

                if row[col].char != ".":

                    cols[col] += 1

        return cols

    def add_move(self, col, char):

        if self.filled_cols[col] < 6:

            self.board[self.filled_cols[col]][col].char = char
            self.filled_cols[col] += 1

        else:

            print("INVALID MOVE")

        return

    def __str__(self):

        ret = "\n---------------\n"

        for i in range(len(self.board)):

            for token in self.board[len(self.board) - i - 1]:

                ret += " " + token.char

            ret += "\n"

        ret += "\n---------------\n"

        return ret

    def get_filled_cols(self):

        return self.filled_cols


class State:
    def __init__(self, board_str):

        self.board = Board(board_str)
        self.score_X = 0
        self.score_O = 0
        self.one_multiplier = 1
        self.two_multiplier = 10
        self.three_multiplier = 100
        self.four_multiplier = 1000
        self.evaluation = None
        self.utility = 0

        return

    def utility(self):

        # TODO

        # if red is winner, return 10000
        # if yellow is winner, return -10000

        return

    def evaluation(self):

        # TODO

        # eval = score(state, red player) - score(state, yellow player)
        # return eval

        return

    def score(self, player):

        # TODO

        # score = number of player tokens
        # score += 10 * num_in_a_row(2, state, player)
        # score += 100 * num_in_a_row(3, state, player)
        # score += 1000 * num_in_a_row(4 or more, state, player)
        # return score

        return

    def num_in_a_row(self, count, player):

        # return the number of times there exists count-in-a-row for player in
        # state

        # When checking a coordinate row-col, we first check horizontally. We
        # track two variables, the first being the number of same tokens to the
        # left (or right) as well as if the token to the left is empty or not.

        # We can then add the left and right together.
        # WE can also check if the left or right was empty, we don't need to
        # check the upper diagonals as no token can exist there.

        # There has to be some sort of iterative solution we can build. Maybe we
        # track the left and upper slots. AS we move right, we continually add
        # to the horizontal count until we hit a blank or other coloured token.
        # As we move up, we add until we hit nothing or the other token. When we
        # do, we count the number in a row.

        # So we set/check 4 values: right, upper right, upper, upper left.

        return

    def update_score(self, token, index):

        if index == -1:

            # print(f"Adding 1 to {token.char}")

            if token.char == "X":

                self.score_X += self.one_multiplier

            else:

                self.score_O += self.one_multiplier

        else:

            if token.directions[index] == 1:

                return

            elif token.directions[index] == 2:

                # print(f"Adding 10 to {token.char}")

                if token.char == "X":

                    self.score_X += self.two_multiplier

                else:

                    self.score_O += self.two_multiplier

            elif token.directions[index] == 3:

                # print(f"Adding 100 to {token.char}")

                if token.char == "X":

                    self.score_X += self.three_multiplier

                else:

                    self.score_O += self.three_multiplier

            elif token.directions[index] >= 4:

                # print(f"Adding 1000 to {token.char}")

                if token.char == "X":

                    self.score_X += self.four_multiplier

                else:

                    self.score_O += self.four_multiplier

    def compute_evaluation(self):

        start_col = 0
        end_col = 6

        for row in range(len(self.board.board)):

            last_token = -1

            for col in range(start_col, end_col + 1):

                token = self.board.board[row][col]

                if token.char != ".":

                    last_token = col

                    # print(f"Checking token at {row},{col} : {token.char}")

                    self.update_score(token, -1)

                    # Check right and upper right
                    if col < end_col:

                        if token.char == self.board.board[row][col + 1].char:

                            self.board.board[row][col + 1].directions[0] = (
                                token.directions[0] + 1
                            )

                        else:

                            self.update_score(token, 0)

                        # Upper right
                        if row < 5:

                            if token.char == self.board.board[row + 1][col + 1].char:

                                self.board.board[row + 1][col + 1].directions[1] = (
                                    token.directions[1] + 1
                                )

                            else:

                                self.update_score(token, 1)

                        else:

                            self.update_score(token, 1)

                    else:

                        self.update_score(token, 0)
                        self.update_score(token, 1)

                    # Check upper and upper left
                    if row < 5:

                        if token.char == self.board.board[row + 1][col].char:

                            self.board.board[row + 1][col].directions[2] = (
                                token.directions[2] + 1
                            )

                        else:

                            self.update_score(token, 2)

                        # Check upper left
                        if col > start_col:

                            if token.char == self.board.board[row + 1][col - 1].char:

                                self.board.board[row + 1][col - 1].directions[3] = (
                                    token.directions[3] + 1
                                )

                            else:

                                self.update_score(token, 3)

                        else:

                            self.update_score(token, 3)

                    else:

                        self.update_score(token, 2)
                        self.update_score(token, 3)

                # If token is blank, update first and last col.
                else:

                    if col == start_col + 1:

                        start_col = col

                    if col == end_col:

                        end_col = last_token

            if last_token == -1:

                break

        # Evaluation
        self.evaluation = self.score_X - self.score_O

        return

    def print_evaluation(self):

        print(f"Score X: {self.score_X}")
        print(f"Score O: {self.score_O}")
        print(f"Evaluation: {self.evaluation}")

        return
