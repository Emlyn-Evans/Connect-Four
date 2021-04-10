class Token:
    def __init__(self, char):

        self.char = char

        # r = 0, ur = 1, u = 2, ul = 3
        self.directions = [1, 1, 1, 1]


class Board:
    def __init__(self):

        self.grid = []
        self.filled_cols = [0, 0, 0, 0, 0, 0, 0]
        self.one_multiplier = 1
        self.two_multiplier = 10
        self.three_multiplier = 100
        self.four_multiplier = 1000

    def compute_filled_cols(self):

        for row in self.grid:

            for col in range(len(row)):

                if row[col].char != ".":

                    # print(f"Adding 1 to col {col}")

                    self.filled_cols[col] += 1

        return

    def create_board_from_str(self, board_str):

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

            self.grid.append(row)

        self.compute_filled_cols()

        return

    def add_move(self, col, char):

        if self.filled_cols[col] < 6:

            token = self.get_token(col)
            token.char = char
            self.filled_cols[col] += 1

        else:

            raise ValueError(f"INVALID MOVE in col {col}")

        return

    def remove_move(self, col):

        if self.filled_cols[col] > 0:

            self.filled_cols[col] -= 1
            token = self.get_token(col)
            token.char = "."

        else:

            raise ValueError(f"INVALID RE-MOVE in col {col}")

        return

    def get_token(self, col, row=None):

        if row is None:

            row = self.filled_cols[col]

        return self.grid[row][col]

    def __str__(self):

        ret = "\n---------------\n"

        for i in range(len(self.grid)):

            for token in self.grid[len(self.grid) - i - 1]:

                ret += " " + token.char

            ret += "\n"

        ret += "\n---------------\n"

        return ret


class State:
    def __init__(self, name, last_move, parent=None):

        self.name = name
        self.last_move = last_move
        self.score_X = 0
        self.score_O = 0
        self.evaluation = 0
        self.utility = 0
        self.parent = parent
        self.children = []
        self.value = None
        self.opt_child = None

    def compute_score(self, board, token, index):

        if index == -1:

            # print(f"Adding 1 to {token.char}")

            if token.char == "X":

                self.score_X += board.one_multiplier

            else:

                self.score_O += board.one_multiplier

        else:

            if token.directions[index] == 1:

                return

            elif token.directions[index] == 2:

                # print(f"Adding 10 to {token.char}")

                if token.char == "X":

                    self.score_X += board.two_multiplier

                else:

                    self.score_O += board.two_multiplier

            elif token.directions[index] == 3:

                # print(f"Adding 100 to {token.char}")

                if token.char == "X":

                    self.score_X += board.three_multiplier

                else:

                    self.score_O += board.three_multiplier

            elif token.directions[index] >= 4:

                # print(f"Adding 1000 to {token.char}")

                if token.char == "X":

                    self.score_X += board.four_multiplier
                    self.utility = 10000

                else:

                    self.score_O += board.four_multiplier
                    self.utility = -10000

    def compute_evaluation(self, board):

        start_col = 0
        end_col = 6

        for row in range(len(board.grid)):

            last_token = -1

            for col in range(start_col, end_col + 1):

                token = board.get_token(col, row)

                if token.char != ".":

                    last_token = col

                    self.compute_score(board, token, -1)

                    # Check right and upper right
                    if col < end_col:

                        r = board.get_token(col + 1, row)
                        if token.char == r.char:

                            r.directions[0] = token.directions[0] + 1

                        else:

                            self.compute_score(board, token, 0)

                        # Upper right
                        if row < 5:

                            ur = board.get_token(col + 1, row + 1)
                            if token.char == ur.char:

                                ur.directions[1] = token.directions[1] + 1

                            else:

                                self.compute_score(board, token, 1)

                        else:

                            self.compute_score(board, token, 1)

                    else:

                        self.compute_score(board, token, 0)
                        self.compute_score(board, token, 1)

                    # Check upper and upper left
                    if row < 5:

                        u = board.get_token(col, row + 1)
                        if token.char == u.char:

                            u.directions[2] = token.directions[2] + 1

                        else:

                            self.compute_score(board, token, 2)

                        # Check upper left
                        if col > start_col:

                            ul = board.get_token(col - 1, row + 1)
                            if token.char == ul.char:

                                ul.directions[3] = token.directions[3] + 1

                            else:

                                self.compute_score(board, token, 3)

                        else:

                            self.compute_score(board, token, 3)

                    else:

                        self.compute_score(board, token, 2)
                        self.compute_score(board, token, 3)

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

    def update_score(self, board, token, num, weight):

        if num == -1:

            if token.char == "X":

                self.score_X += board.one_multiplier

            else:

                self.score_O += board.one_multiplier

        elif num == 1:

            return

        elif num == 2:

            if token.char == "X":

                self.score_X += board.two_multiplier * weight

            else:

                self.score_O += board.two_multiplier * weight

        elif num == 3:

            if token.char == "X":

                self.score_X += board.three_multiplier * weight

            else:

                self.score_O += board.three_multiplier * weight

        elif num >= 4:

            if token.char == "X":

                self.score_X += board.four_multiplier * weight
                self.utility = 10000

            else:

                self.score_O += board.four_multiplier * weight
                self.utility = -10000

    def update_evaluation(self, board, col):

        row = board.filled_cols[col] - 1
        token = board.get_token(col, row)

        self.update_score(board, token, -1, 1)

        # Check horizontal

        i = col
        j = row
        n_horizontal = 1
        n_prev = 0

        while i > 0:

            next_token = board.get_token(i - 1, j)

            if next_token.char == token.char:
                n_horizontal += 1
                n_prev += 1
                i -= 1

            else:
                i = 0

        # Minus prev
        self.update_score(board, token, n_prev, -1)

        i = col
        n_prev = 0

        while i < 6:

            next_token = board.get_token(i + 1, j)

            if next_token.char == token.char:
                n_horizontal += 1
                n_prev += 1
                i += 1

            else:
                i = 6

        self.update_score(board, token, n_prev, -1)
        self.update_score(board, token, n_horizontal, 1)

        # Check vertical
        i = col
        n_vertical = 1
        n_prev = 0

        while j > 0:

            next_token = board.get_token(i, j - 1)

            if next_token.char == token.char:
                n_vertical += 1
                n_prev += 1
                j -= 1

            else:
                j = 0

        self.update_score(board, token, n_prev, -1)

        j = row
        n_prev = 0

        while j < 6:

            next_token = board.get_token(i, j + 1)

            if next_token.char == token.char:
                n_vertical += 1
                n_prev += 1
                j += 1

            else:
                j = 6

        self.update_score(board, token, n_prev, -1)
        self.update_score(board, token, n_vertical, 1)

        # Check left diagonal
        j = row
        n_prev = 0
        n_major_diagonal = 1

        while j > 0 and i < 6:

            next_token = board.get_token(i + 1, j - 1)

            if next_token.char == token.char:
                n_major_diagonal += 1
                n_prev += 1
                i += 1
                j -= 1

            else:
                i = 6

        self.update_score(board, token, n_prev, -1)

        i = col
        j = row
        n_prev = 0

        while j < 6 and i > 0:

            next_token = board.get_token(i - 1, j + 1)

            if next_token.char == token.char:
                n_major_diagonal += 1
                n_prev += 1
                i -= 1
                j += 1

            else:
                i = 0

        self.update_score(board, token, n_prev, -1)
        self.update_score(board, token, n_major_diagonal, 1)

        # Check right diagonal

        i = col
        j = row
        n_minor_diagonal = 1
        n_prev = 0

        while j > 0 and i > 0:

            next_token = board.get_token(i - 1, j - 1)

            if next_token.char == token.char:
                n_minor_diagonal += 1
                n_prev += 1
                i -= 1
                j -= 1

            else:
                i = 0

        self.update_score(board, token, n_prev, -1)

        i = col
        j = row
        n_prev = 0

        while j < 6 and i < 6:

            next_token = board.get_token(i + 1, j + 1)

            if next_token.char == token.char:
                n_minor_diagonal += 1
                n_prev += 1
                i += 1
                j += 1

            else:
                i = 6

        self.update_score(board, token, n_prev, -1)
        self.update_score(board, token, n_minor_diagonal, 1)

        self.evaluation = self.score_X - self.score_O

        return

    def add_child(self, board, col):

        last_move = None

        if self.last_move == "X":

            last_move = "O"

        else:

            last_move = "X"

        child = State(self.name + str(col), last_move, self)
        child.score_X = self.score_X
        child.score_O = self.score_O

        child.update_evaluation(board, col)

        self.children.append(child)

        return child

    def __str__(self):

        ret = f"\nState: {self.name}\nScore X: {self.score_X}\n"
        ret += f"Score O: {self.score_O}\n"
        ret += f"Eval: {self.evaluation} | Utility: {self.utility}\n"
        ret += f"Value: {self.value} | Optimal Child: {self.opt_child}\n"

        return ret
