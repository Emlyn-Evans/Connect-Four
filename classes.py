class Board:
    def __init__(self, player):

        self.rows = 6
        self.cols = 7
        self.player = player
        self.pos = None
        self.board = None
        self.moves_player = 0
        self.moves_board = 0
        self.n_nodes = 0
        self.n_terminal = 0
        self.n_depth = 0
        self.order = [3, 2, 4, 1, 5, 0, 6]
        self.bit_bottom = self.compute_bit_bottom()
        self.last_node = None
        self.max_utility = int((self.rows * self.cols + 1) / 2) - 3
        self.min_utility = -int((self.rows * self.cols) / 2) + 3

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

        if self.player == "O":

            self.pos = self.pos ^ self.board
            self.moves_player = self.moves_board - self.moves_player

        return

    def check_win(self, player):

        num = None

        if player == self.player:

            num = self.pos

        else:

            num = self.get_opponent_pos()

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

            # # If that move is the current player move
            # if int(self.get_bin(self.pos)[self.coord_to_index(0, col)]):

            #     self.switch_player()

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
        self.pos = self.pos ^ self.board
        self.moves_player = self.moves_board - self.moves_player
        self.player = self.get_opponent()

        return

    def get_opponent(self):

        player = None

        if self.player == "X":

            player = "O"

        else:

            player = "X"

        return player

    def check_filled(self, col):

        index = self.coord_to_index(self.rows - 1, col)
        ret = int(self.get_bin(self.board)[index])
        # print(f"Index: {index} | Bit: {ret}")

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

    def compute_bit_bottom(self):

        num = 1

        for i in range(self.cols - 1):

            num = num << (self.rows + 1)
            num += 1

        return num

    def bit_possible(self):

        num = (self.board + self.bit_bottom) & (~(self.bit_bottom << self.rows))
        # print(f"Possible: {self.get_bin(num)}")

        return num

    def bit_winning_map(self, pos=None):

        if pos is None:

            pos = self.pos

        # Need to add in X.XX positions:
        # (pos & (pos << 1)) & (pos << 2)

        # Vertical
        win = (pos << 1) & (pos << 2) & (pos << 3)

        # Horizontal
        # Here we need to account for cases with gaps: ..XX.X..
        pos_base = (pos << (self.rows + 1)) & (pos << (self.rows + 1) * 2)
        win = win | (pos_base & (pos << (self.rows + 1) * 3))
        win = win | (pos_base & (pos >> (self.rows + 1)))

        pos_base = (pos >> (self.rows + 1)) & (pos >> (self.rows + 1) * 2)
        win = win | (pos_base & (pos >> (self.rows + 1) * 3))
        win = win | (pos_base & (pos << (self.rows + 1)))

        # print(f"Pos:            {self.get_bin(pos)}")
        # print(f"Pos < 1:        {self.get_bin(pos << (self.rows + 1))}")
        # print(f"Pos < 2:        {self.get_bin(pos << ((self.rows + 1) * 2))}")
        # print(f"Pos_1 & Pos_2:  {self.get_bin(pos_base)}")
        # print(f"Pos < 3:        {self.get_bin(pos << ((self.rows + 1) * 3))}")
        # print(f"Pos > 1:        {self.get_bin(pos >> (self.rows + 1))}")
        # print(f"Horizontal:     {self.get_bin(win)}")

        # Major Diagonal

        pos_base = (pos << self.rows) & (pos << (self.rows * 2))
        win = win | (pos_base & (pos << (self.rows * 3)))
        win = win | (pos_base & (pos >> self.rows))

        pos_base = (pos >> self.rows) & (pos >> (self.rows * 2))
        win = win | (pos_base & (pos >> (self.rows * 3)))
        win = win | (pos_base & (pos << self.rows))

        # Minor Diagonal

        pos_base = (pos << (self.rows + 2)) & (pos << ((self.rows + 2) * 2))
        win = win | (pos_base & (pos << ((self.rows + 2) * 3)))
        win = win | (pos_base & (pos >> (self.rows + 2)))

        pos_base = (pos >> (self.rows + 2)) & (pos >> ((self.rows + 2) * 2))
        win = win | (pos_base & (pos >> ((self.rows + 2) * 3)))
        win = win | (pos_base & (pos << (self.rows + 2)))

        # print(f"Win:     {self.get_bin(win)}")

        return win

    def bit_winning_col(self, pos=None):

        if pos is None:

            pos = self.pos

        result = self.bit_winning_map(pos) & self.bit_possible()

        col = None

        for i in range(self.cols):

            if (self.bit_col(i) & result) != 0:

                col = i

        # print(f"WINNING COL: {col}")

        return col

    def bit_potential_map(self):

        opponent_win = self.bit_winning_map(self.get_opponent_pos())
        possible = self.bit_possible()
        forced_moves = opponent_win & possible

        if forced_moves != 0:

            if forced_moves & (forced_moves - 1) != 0:

                # We lose no matter what we play
                return 0

            else:

                return forced_moves

        else:

            # We don't want to play in a column where an opponent can win next
            # turn

            safe_map = self.bit_possible() & (~(opponent_win >> 1))

            return safe_map

    def bit_col(self, col):

        return ((1 << self.rows) - 1) << ((self.rows + 1) * col)

    def bit_score_move(self, move_map):

        # We build an evaluation function here
        # We start by scoring the number of open 3-in-a-row-positions

        chances = self.bit_winning_map(self.pos | move_map)
        available_chances = (
            chances & (~(self.bit_bottom << self.rows)) & (~(self.board))
        )

        return self.count_ones(available_chances)

    def get_opponent_pos(self):

        return self.board ^ self.pos

    def get_bin(self, num):

        return f"{num:049b}"

    def get_key(self):

        return self.board + self.pos

    def get_utility(self):

        return int((self.rows * self.cols - self.moves_board) / 2)

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


class Node:
    def __init__(self, name, player, depth, parent=None):

        self.name = name
        self.player = player
        self.depth = depth
        self.utility = None
        self.value = None
        self.parent = parent
        self.children = []
        self.n_children = 0
        self.opt_child = None
        self.opt_col = None
        self.opt_string = ""

    def add_child(self, board, col):

        # We operate as if the move has already been made in the board
        child = Node(self.name + str(col), board.player, self.depth + 1, self)
        self.children.append(child)
        self.n_children += 1

        return child

    def __str__(self):

        ret = f"Node: {self.name} | Turn: {self.player} | Utility: {self.utility} | "
        ret += f"Value: {self.value} | Optimal Col: {self.opt_col}"

        return ret


class Trans_Table:
    def __init__(self, max_size):

        self.table = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def add(self, key, value):

        self.table[self.get_index(key)] = value

    def get_index(self, key):

        return key % self.max_size

    def get_value(self, key):

        if self.get_index(key) not in self.table:

            self.misses += 1

            return None

        else:

            self.hits += 1

            return self.table[self.get_index(key)]


class Move_Sorter:
    def __init__(self):

        self.cols = [0, 0, 0, 0, 0, 0, 0]
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.size = 0
        self.index = 0
        self.col_order = [3, 2, 4, 1, 5, 0, 6]

    def compute_move_order(self, potential_map, board):

        for col in self.col_order:

            move_map = board.bit_col(col) & potential_map

            if move_map != 0:

                score = board.bit_score_move(move_map)

                # print(f"Col: {col} : Score: {score}")
                # print(f"Cols: {self.cols} : Scores: {self.scores}")

                # Add to array

                index = self.size

                # Modified insertion sort
                while index > 0 and self.scores[index - 1] < score:

                    self.cols[index] = self.cols[index - 1]
                    self.scores[index] = self.scores[index - 1]
                    index -= 1

                self.cols[index] = col
                self.scores[index] = score
                self.size += 1

        return

    def get_next_move(self):

        if self.index < self.size:

            col = self.cols[self.index]
            self.index += 1

            return col

        return None

    def reset(self):

        self.cols = [0, 0, 0, 0, 0, 0, 0]
        self.scores = [0, 0, 0, 0, 0, 0, 0]
        self.size = 0
        self.index = 0


class Book:
    def __init__(self):

        self.oracle = {}

    def get_key(self, board_str):

        player_bits = ""
        board_bits = ""

        rows = board_str.split(",")

        for j in range(6, -1, -1):

            player_bits += "0"
            board_bits += "0"

            for i in range(5, -1, -1):

                if rows[i][j] == "r":

                    player_bits += "1"
                    board_bits += "1"

                elif rows[i][j] == "y":

                    player_bits += "0"
                    board_bits += "1"

                else:

                    player_bits += "0"
                    board_bits += "0"

        pos = int(player_bits, 2)
        board = int(board_bits, 2)

        return pos + board

    def input_oracle(self):

        text = input("Enter action: ")

        legit = True

        while text is legit:

            text_list = text.split(" ")

            if len(text_list) == 2:

                action = text_list[0]
                col = int(text_list[1])

                if action == "a":

                    if col < 7 and col >= 0:

                        # Add move to board
                        return

                    else:

                        legit = False

                elif action == "r":

                    if col < 7 and col >= 0:

                        # Remove move from board

                    else:

                        legit = False

                else:

                    legit = False

    def build_oracle(self):

        # r_0_0 = ".......,.......,.......,.......,.......,......."
        self.oracle[self.get_key(".......,.......,.......,.......,.......,.......")] = 3

        # 1
        self.oracle[
            self.get_key("r......,.......,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key(".r.....,.......,.......,.......,.......,.......")
        ] = 2  # 2
        self.oracle[
            self.get_key("..r....,.......,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key("...r...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key("....r..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key(".....r.,.......,.......,.......,.......,.......")
        ] = 4  # 4
        self.oracle[
            self.get_key("......r,.......,.......,.......,.......,.......")
        ] = 3  # 3

        # 2
        self.oracle[
            self.get_key("y..r...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key(".y.r...,.......,.......,.......,.......,.......")
        ] = 1  # 1
        self.oracle[
            self.get_key("..yr...,.......,.......,.......,.......,.......")
        ] = 5  # 5
        self.oracle[
            self.get_key("...r...,...y...,.......,.......,.......,.......")
        ] = 3  # 3
        self.oracle[
            self.get_key("...ry..,.......,.......,.......,.......,.......")
        ] = 1  # 1
        self.oracle[
            self.get_key("...r.y.,.......,.......,.......,.......,.......")
        ] = 5  # 5
        self.oracle[
            self.get_key("...r..y,.......,.......,.......,.......,.......")
        ] = 3  # 3

        # 3
        y_3_030 = self.oracle[
            self.get_key("r..y...,r......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_031 = self.oracle[
            self.get_key("rr.y...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_032 = self.oracle[
            self.get_key("r.ry...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_033 = self.oracle[
            self.get_key("r..y...,...r...,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_034 = self.oracle[
            self.get_key("r..yr..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_035 = self.oracle[
            self.get_key("r..y.r.,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_036 = self.oracle[
            self.get_key("r..y..r,.......,.......,.......,.......,.......")
        ] = 2  # 2

        y_3_120 = self.oracle[
            self.get_key("rry....,.......,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_121 = self.oracle[
            self.get_key(".ry....,.r.....,.......,.......,.......,.......")
        ] = 1  # 1
        y_3_122 = self.oracle[
            self.get_key(".ry....,..r....,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_123 = self.oracle[
            self.get_key(".ryr...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_124 = self.oracle[
            self.get_key(".ry.r..,.......,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_125 = self.oracle[
            self.get_key(".ry..r.,.......,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_126 = self.oracle[
            self.get_key(".ry...r,.......,.......,.......,.......,.......")
        ] = 2  # 2

        y_3_230 = self.oracle[
            self.get_key("r.ry...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_231 = self.oracle[
            self.get_key(".rry...,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_232 = self.oracle[
            self.get_key("..ry...,..r....,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_233 = self.oracle[
            self.get_key("..ry...,...r...,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_234 = self.oracle[
            self.get_key("..ryr..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_235 = self.oracle[
            self.get_key("..ry.r.,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_236 = self.oracle[
            self.get_key("..ry..r,.......,.......,.......,.......,.......")
        ] = 3  # 3

        y_3_330 = self.oracle[
            self.get_key("r..r...,...y...,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_331 = self.oracle[
            self.get_key(".r.r...,...y...,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_332 = self.oracle[
            self.get_key("..rr...,...y...,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_333 = self.oracle[
            self.get_key("...r...,...y...,...r...,.......,.......,.......")
        ] = 3  # 3
        y_3_334 = self.oracle[
            self.get_key("...rr..,...y...,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_335 = self.oracle[
            self.get_key("...r.r.,...y...,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_336 = self.oracle[
            self.get_key("...r..r,...y...,.......,.......,.......,.......")
        ] = 3  # 3

        y_3_430 = self.oracle[
            self.get_key("r..yr..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_431 = self.oracle[
            self.get_key(".r.yr..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_432 = self.oracle[
            self.get_key("..ryr..,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_433 = self.oracle[
            self.get_key("...yr..,...r...,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_434 = self.oracle[
            self.get_key("...yr..,....r..,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_435 = self.oracle[
            self.get_key("...yrr.,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_436 = self.oracle[
            self.get_key("...yr.r,.......,.......,.......,.......,.......")
        ] = 3  # 3

        y_3_540 = self.oracle[
            self.get_key("r...yr.,.......,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_541 = self.oracle[
            self.get_key(".r..yr.,.......,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_542 = self.oracle[
            self.get_key("..r.yr.,.......,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_543 = self.oracle[
            self.get_key("...ryr.,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_544 = self.oracle[
            self.get_key("....yr.,....r..,.......,.......,.......,.......")
        ] = 4  # 4
        y_3_545 = self.oracle[
            self.get_key("....yr.,.....r.,.......,.......,.......,.......")
        ] = 5  # 5
        y_3_546 = self.oracle[
            self.get_key("....yrr,.......,.......,.......,.......,.......")
        ] = 4  # 4

        y_3_630 = self.oracle[
            self.get_key("r..y..r,.......,.......,.......,.......,.......")
        ] = 2  # 2
        y_3_631 = self.oracle[
            self.get_key(".r.y..r,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_632 = self.oracle[
            self.get_key("..ry..r,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_633 = self.oracle[
            self.get_key("...y..r,...r...,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_634 = self.oracle[
            self.get_key("...yr.r,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_635 = self.oracle[
            self.get_key("...y.rr,.......,.......,.......,.......,.......")
        ] = 3  # 3
        y_3_636 = self.oracle[
            self.get_key("...y..r,......r,.......,.......,.......,.......")
        ] = 3  # 3

        # 4

        # self.oracle[]
