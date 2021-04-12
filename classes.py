class Board:
    def __init__(self, player):

        self.rows = 6
        self.cols = 7
        self.player = player
        self.pos = None
        self.board = None
        self.moves_player = None
        self.moves_board = None

    def create_board_from_str(self, board_str):

        player_bits = ""
        board_bits = ""
        moves_player = 0
        moves_board = 0

        rows = board_str.split(",")

        for j in range(self.cols - 1, -1, -1):

            player_bits += "0"
            board_bits += "0"

            for i in range(self.rows - 1, -1, -1):

                if rows[i][j] == "r":

                    player_bits += "1"
                    board_bits += "1"
                    moves_player += 1
                    moves_board += 1

                elif rows[i][j] == "y":

                    player_bits += "0"
                    board_bits += "1"
                    moves_board += 1

                else:

                    player_bits += "0"
                    board_bits += "0"

        self.pos = int(player_bits, 2)
        self.board = int(board_bits, 2)
        self.moves_player = moves_player
        self.moves_board = moves_board

        return

    def check_win(self, player):

        num = None

        if player == self.player:

            num = self.pos

        else:

            num = self.board ^ self.pos

        # Horizontal
        mask = num & num >> 7
        result = mask & mask >> 14

        if result != 0:

            return True

        # Vertical
        mask = num & num >> 1
        result = mask & mask >> 2

        if result != 0:

            return True

        # Major diagonal
        mask = num & num >> 6
        result = mask & mask >> 12

        if result != 0:

            return True

        # Minor diagonal
        mask = num & num >> 8
        result = mask & mask >> 16

        if result != 0:

            return True

        return False

    def add_move(self, col):

        # Check if legal move
        if self.check_filled(col) == 0:

            self.moves_player += 1
            self.moves_board += 1

            # Switch player and add move to board
            self.switch_player()
            # print(f"Slot:              {self.get_bin(1 << (7 * col))}")
            # print(f"Board + Slot:      {self.get_bin(self.board + (1 << (7 * col)))}")
            # print(f"OR: Board before:  {self.get_bin(self.board)}")
            self.board = self.board | self.board + (1 << (7 * col))
            # print(f"Result:            {self.get_bin(self.board)}")

        else:

            print("INVALID MOVE IN FILLED COLUMN")

        return

    def remove_move(self, col):

        # If the board has a move in the column
        if int(self.get_bin(self.board)[self.coord_to_index(0, col)]):

            # If that move is the current player move
            if int(self.get_bin(self.pos)[self.coord_to_index(0, col)]):

                self.switch_player()

            # Undo board move
            # print(f"Col:                  {self.get_bin(1 << (7 * col))}")
            # print(f"Board:                {self.get_bin(self.board)}")
            # print(
            #     f"Board + Col:          {self.get_bin(self.board + (1 << (7 * col)))}"
            # )
            # print(
            #     f"B + C ^ B:            {self.get_bin(self.board + (1 << (7 * col)) ^ self.board)}"
            # )
            # print(
            #     f"(B + C ^ B) + C:      {self.get_bin((self.board + (1 << (7 * col)) ^ self.board) + (1 << (7 * col)))}"
            # )
            # print(
            #     f"(B + C ^ B) + C >> 2: {self.get_bin(((self.board + (1 << (7 * col)) ^ self.board) + (1 << (7 * col))) >> 2)}"
            # )

            slot = (
                (self.board + (1 << (7 * col)) ^ self.board) + (1 << (7 * col))
            ) >> 2
            self.board = self.board - slot
            # print(f"Result:               {self.get_bin(self.board)}")
            self.switch_player()

            self.moves_player -= 1
            self.moves_board -= 1

        else:

            print("INVALID RE-MOVE IN EMPTY COLUMN")

        return

    def switch_player(self):

        # Flip the pos
        self.pos = self.get_player_pos(self.player) ^ self.board
        self.moves_player = self.moves_board - self.moves_player

        if self.player == "X":

            self.player = "O"

        else:

            self.player = "X"

        return

    def check_filled(self, col):

        index = self.coord_to_index(self.rows - 1, col)
        ret = int(self.get_bin(self.board)[index])

        return ret

    def coord_to_index(self, row, col):

        index = len(self.get_bin(self.board)) - 1 - ((col * (self.rows + 1)) + row)

        return index

    def count_ones(self, num):

        count = 0

        while num != 0:

            num = num & (num - 1)
            count += 1

        return count

    def get_player_pos(self, player):

        ret = None

        if player == self.player:

            ret = self.pos

        else:

            ret = self.board ^ self.pos

        return ret

    def get_bin(self, num):

        return f"{num:049b}"

    def __str__(self):

        ret = "\n---------------\n"

        for i in range(self.rows - 1, -1, -1):

            for j in range(self.cols):

                if self.get_bin(self.board)[self.coord_to_index(i, j)] == "1":

                    if self.get_bin(self.pos)[self.coord_to_index(i, j)] == "1":

                        ret += f" {self.player}"

                    else:

                        if self.player == "X":

                            ret += " O"

                        else:

                            ret += " X"

                else:

                    ret += " ."

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
