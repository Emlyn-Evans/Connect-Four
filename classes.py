class Board:
    def __init__(self):

        self.rows = 6
        self.cols = 7
        self.x_bits = ""
        self.o_bits = ""
        self.x_num = None
        self.o_num = None

    def create_board_from_str(self, board_str):

        rows = board_str.split(",")

        for i in range(self.rows - 1, -1, -1):

            self.x_bits += "0"
            self.o_bits += "0"

            for j in range(self.cols - 1, -1, -1):

                if rows[i][j] == "r":

                    self.x_bits += "1"
                    self.o_bits += "0"

                elif rows[i][j] == "y":

                    self.x_bits += "0"
                    self.o_bits += "1"

                else:

                    self.x_bits += "0"
                    self.o_bits += "0"

        self.x_num = int(self.x_bits, 2)
        self.o_num = int(self.o_bits, 2)

        return

    def add_move(self, col, char):

        # Check if legal move

        return

    def remove_move(self, col):

        return

    def __str__(self):

        ret = "\n---------------\n"

        offset = 0

        for i in range(self.rows):

            offset = (i + 1) * 8 - 1

            for j in range(self.cols):

                if self.x_bits[offset] == "1":

                    ret += " X"

                elif self.o_bits[offset] == "1":

                    ret += " O"

                else:

                    ret += " ."

                offset -= 1

            ret += "\n"

        ret += "\n---------------\n"

        return ret


# Haven't dealt with this yet


class State:
    def __init__(self, name, move, parent=None):

        self.name = name
        self.move = move
        self.score_X = 0
        self.score_O = 0
        self.evaluation = 0
        self.utility = 0
        self.parent = parent
        self.children = []
        self.value = None
        self.opt_child = None

    def compute_score(self, board, token, index):

        return

    def compute_evaluation(self, board):

        return

    def update_score(self, board, token, num, weight):

        return

    def update_evaluation(self, board, col):

        return

    def add_child(self, board, col):

        return

    def __str__(self):

        ret = f"State: {self.name} | Score X: {self.score_X}"
        ret += f" | Score O: {self.score_O} | "
        ret += f"Eval: {self.evaluation} | Utility: {self.utility} | "
        ret += f"Value: {self.value} | Optimal Child: {self.opt_child} | "

        if self.parent is not None:
            ret += f"Parent value: {self.parent.value}\n"

        return ret
