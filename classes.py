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

        # Bit shifting to check if 4-in-a-row line up

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

        return num

    def bit_winning_map(self, pos=None):

        if pos is None:

            pos = self.pos

        # Need to add in X.XX positions

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

        # Overlap winning positions to see if they are possible
        result = self.bit_winning_map(pos) & self.bit_possible()

        col = None

        for i in range(self.cols):

            if (self.bit_col(i) & result) != 0:

                col = i

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

    def bit_symmetry_key(self):

        pos = self.pos
        board = self.board

        # For col 0 > col 6
        col = self.bit_col(0)
        sym_board = (board & col) << (self.cols * 6)
        sym_pos = (pos & col) << (self.cols * 6)

        # print(f"Symmetrical 0: {self.get_bin(sym_board)}")
        # print(f"Symmetrical 0: {self.get_bin(sym_pos)}")

        # For col 1 > col 5
        col = col << (self.cols)
        sym_board = sym_board | ((board & col) << (self.cols * 4))
        sym_pos = sym_pos | ((pos & col) << (self.cols * 4))

        # For col 2 > col 4
        col = col << (self.cols)
        sym_board = sym_board | ((board & col) << (self.cols * 2))
        sym_pos = sym_pos | ((pos & col) << (self.cols * 2))

        # For col 3
        col = col << (self.cols)
        sym_board = sym_board | (board & col)
        sym_pos = sym_pos | (pos & col)

        # For col 4 < col 2
        col = col << (self.cols)
        sym_board = sym_board | ((board & col) >> (self.cols * 2))
        sym_pos = sym_pos | ((pos & col) >> (self.cols * 2))

        # For col 5 < col 1
        col = col << (self.cols)
        sym_board = sym_board | ((board & col) >> (self.cols * 4))
        sym_pos = sym_pos | ((pos & col) >> (self.cols * 4))

        # For col 6 < col 0
        col = col << (self.cols)
        sym_board = sym_board | ((board & col) >> (self.cols * 6))
        sym_pos = sym_pos | ((pos & col) >> (self.cols * 6))

        sym_key = sym_board + sym_pos

        return sym_key

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
        self.board = None
        self.running = True

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

    def set_board(self, player, board_str):

        self.board = Board(player)
        self.board.create_board_from_str(board_str)
        self.running = True

    def build_oracle(self, move_depth):

        # We only want to create book moves for positions that can't be solved,
        # so that means positions that take more than 10 moves per player to win

        looping = True

        while self.running and looping:

            key = self.board.get_key()
            sym_key = self.board.bit_symmetry_key()

            if key not in self.oracle and sym_key not in self.oracle:

                print(self.board)

                text = input("Optimum Col: ")

                if text == "":

                    text = input("Are you sure you want to exit?: ")

                    if text == "":

                        self.running = False

                        return

                else:

                    if text == "s":

                        # Solvable position, so don't need to add to oracle
                        looping = False
                        return

                    else:

                        try:

                            opt_col = int(text)

                        except ValueError:

                            print("Invalid input, try again")

                            continue

                        # Add to oracle
                        self.oracle[key] = opt_col

            looping = False

            if self.board.moves_player >= move_depth:

                return

            if key in self.oracle:

                play_col = self.oracle[key]

            elif sym_key in self.oracle:

                play_col = 6 - self.oracle[sym_key]

            self.board.add_move(play_col)

            # Get next board config
            move_sorter = Move_Sorter()
            potential_map = self.board.bit_potential_map()
            move_sorter.compute_move_order(potential_map, self.board)
            col = move_sorter.get_next_move()

            while col is not None:

                # Make child with col
                self.board.add_move(col)
                self.build_oracle(move_depth)
                self.board.remove_move(col)

                col = move_sorter.get_next_move()

            self.board.remove_move(play_col)

        return

    def write_oracle(self, filepath):

        with open(filepath, "a") as file:

            file.write("\n-------------------------\n\n")

            for key in self.oracle:

                line = f"self.oracle[{key}] = {self.oracle[key]}\n"
                file.write(line)

    def fix_mistakes(self):

        # Mistakes - override
        self.oracle[self.get_key("..yr.r.,.....y.,.......,.......,.......,.......")] = 6
        self.oracle[self.get_key("r.ry...,..yy...,...r...,...r...,.......,.......")] = 0
        self.oracle[self.get_key(".ryr.rr,..yy...,.......,.......,.......,.......")] = 4
        self.oracle[self.get_key("r.ry...,...r...,...y...,...r...,...y...,.......")] = 3

    def read_oracle(self):

        # Optimal moves for 4 moves each
        self.oracle[0] = 3
        self.oracle[8388608] = 3
        self.oracle[41943040] = 3
        self.oracle[25182208] = 3
        self.oracle[25165952] = 3
        self.oracle[25165825] = 4
        self.oracle[4210688] = 5
        self.oracle[68727881728] = 3
        self.oracle[68723720192] = 2
        self.oracle[68992122880] = 4
        self.oracle[68723687552] = 3
        self.oracle[137443164160] = 6
        self.oracle[68723687425] = 3
        self.oracle[4466770198528] = 5
        self.oracle[4194432] = 1
        self.oracle[8389248] = 3
        self.oracle[4211328] = 1
        self.oracle[272630400] = 3
        self.oracle[4195456] = 3
        self.oracle[34363933312] = 3
        self.oracle[4194945] = 4
        self.oracle[4398050706048] = 3
        self.oracle[4194305] = 3
        self.oracle[20971521] = 3
        self.oracle[12599297] = 3
        self.oracle[281018369] = 3
        self.oracle[12583041] = 3
        self.oracle[34372321281] = 3
        self.oracle[12582915] = 3
        self.oracle[4398059094017] = 3
        self.oracle[1] = 3
        self.oracle[8388609] = 3
        self.oracle[41943041] = 5
        self.oracle[25182209] = 2
        self.oracle[293601281] = 3
        self.oracle[25165953] = 3
        self.oracle[34384904193] = 3
        self.oracle[25165827] = 3
        self.oracle[4398071676929] = 3
        self.oracle[4210689] = 3
        self.oracle[20987905] = 2
        self.oracle[12632065] = 3
        self.oracle[281034753] = 3
        self.oracle[12599425] = 3
        self.oracle[34372337665] = 3
        self.oracle[12599299] = 3
        self.oracle[4398059110401] = 3
        self.oracle[272629761] = 3
        self.oracle[289406977] = 4
        self.oracle[817889281] = 3
        self.oracle[281018497] = 3
        self.oracle[34640756737] = 3
        self.oracle[281018371] = 3
        self.oracle[4194433] = 3
        self.oracle[20971649] = 1
        self.oracle[12583297] = 3
        self.oracle[34372321409] = 3
        self.oracle[12583043] = 3
        self.oracle[4398059094145] = 3
        self.oracle[34363932673] = 3
        self.oracle[34380709889] = 3
        self.oracle[103091798017] = 3
        self.oracle[34372321283] = 4
        self.oracle[4194307] = 3
        self.oracle[12582919] = 0
        self.oracle[20971523] = 4
        self.oracle[4398059094019] = 3
        self.oracle[4398050705409] = 4
        self.oracle[4398591770625] = 2
        self.oracle[4398587592705] = 4
        self.oracle[4399124447233] = 2
        self.oracle[4398587576449] = 3
        self.oracle[4432947314689] = 3
        self.oracle[4398587576323] = 2
        self.oracle[13194680598529] = 2
        self.oracle[128] = 2
        self.oracle[2130048] = 3
        self.oracle[18907264] = 2
        self.oracle[10551424] = 3
        self.oracle[278954112] = 3
        self.oracle[10518912] = 3
        self.oracle[34370257024] = 3
        self.oracle[10518657] = 3
        self.oracle[4398057029760] = 3
        self.oracle[65664] = 2
        self.oracle[2293888] = 3
        self.oracle[327808] = 1
        self.oracle[268632192] = 2
        self.oracle[196992] = 2
        self.oracle[34359935104] = 3
        self.oracle[196737] = 2
        self.oracle[4398046707840] = 2
        self.oracle[268468352] = 2
        self.oracle[270631040] = 3
        self.oracle[268599424] = 2
        self.oracle[805404800] = 4
        self.oracle[268534144] = 2
        self.oracle[34628272256] = 2
        self.oracle[268533889] = 2
        self.oracle[4398315044992] = 2
        self.oracle[33152] = 1
        self.oracle[2131328] = 3
        self.oracle[66944] = 2
        self.oracle[268469632] = 2
        self.oracle[35200] = 2
        self.oracle[34359772544] = 2
        self.oracle[34177] = 2
        self.oracle[4398046545280] = 3
        self.oracle[34359771264] = 2
        self.oracle[34361933952] = 3
        self.oracle[34359902336] = 2
        self.oracle[34359837056] = 2
        self.oracle[103079313536] = 1
        self.oracle[34359836801] = 2
        self.oracle[4432406347904] = 3
        self.oracle[32897] = 2
        self.oracle[2195585] = 2
        self.oracle[163969] = 2
        self.oracle[98689] = 2
        self.oracle[98435] = 2
        self.oracle[4398046609537] = 2
        self.oracle[4398046544000] = 2
        self.oracle[4398048706688] = 3
        self.oracle[4398046675072] = 2
        self.oracle[4398046609792] = 2
        self.oracle[13194139631744] = 2
        self.oracle[16384] = 3
        self.oracle[8404992] = 3
        self.oracle[41959424] = 3
        self.oracle[25214976] = 3
        self.oracle[293617664] = 3
        self.oracle[25182336] = 3
        self.oracle[34384920576] = 3
        self.oracle[4243456] = 2
        self.oracle[8568832] = 3
        self.oracle[4505600] = 3
        self.oracle[272809984] = 3
        self.oracle[4374656] = 3
        self.oracle[34364112896] = 3
        self.oracle[4374529] = 3
        self.oracle[4398050885632] = 3
        self.oracle[272646144] = 3
        self.oracle[289423360] = 3
        self.oracle[281067520] = 3
        self.oracle[281034880] = 3
        self.oracle[4210816] = 3
        self.oracle[20988032] = 3
        self.oracle[12632192] = 3
        self.oracle[12599680] = 3
        self.oracle[34372337792] = 3
        self.oracle[34363949056] = 3
        self.oracle[34380726272] = 3
        self.oracle[34372370432] = 3
        self.oracle[103091814400] = 3
        self.oracle[2097152] = 3
        self.oracle[18874368] = 3
        self.oracle[85983232] = 2
        self.oracle[52445184] = 4
        self.oracle[52428928] = 2
        self.oracle[52428801] = 2
        self.oracle[10502144] = 4
        self.oracle[547373184] = 0
        self.oracle[547373057] = 1
        self.oracle[555761664] = 4
        self.oracle[547405824] = 2
        self.oracle[1084243968] = 3
        self.oracle[4398593884160] = 4
        self.oracle[10485888] = 2
        self.oracle[10485761] = 3
        self.oracle[27279361] = 1
        self.oracle[27263105] = 2
        self.oracle[44040193] = 2
        self.oracle[295698433] = 3
        self.oracle[34387001345] = 3
        self.oracle[27262979] = 3
        self.oracle[4398073774081] = 3
        self.oracle[176160768] = 2
        self.oracle[109068288] = 2
        self.oracle[109052032] = 1
        self.oracle[109051905] = 2
        self.oracle[92291072] = 2
        self.oracle[58769408] = 3
        self.oracle[327172096] = 3
        self.oracle[58736768] = 3
        self.oracle[34418475008] = 3
        self.oracle[58736641] = 3
        self.oracle[4398105247744] = 3
        self.oracle[92274816] = 1
        self.oracle[58720640] = 3
        self.oracle[34418458752] = 3
        self.oracle[58720385] = 3
        self.oracle[4398105231488] = 3
        self.oracle[578813953] = 2
        self.oracle[562053121] = 3
        self.oracle[1098907649] = 2
        self.oracle[562036865] = 5
        self.oracle[34921775105] = 3
        self.oracle[562036739] = 2
        self.oracle[4398608547841] = 2
        self.oracle[68761436160] = 6
        self.oracle[68744691712] = 5
        self.oracle[69013094400] = 3
        self.oracle[68744659072] = 3
        self.oracle[137464135680] = 3
        self.oracle[68744658945] = 3
        self.oracle[4466791170048] = 3
        self.oracle[68728045568] = 3
        self.oracle[68723982336] = 3
        self.oracle[68992286720] = 4
        self.oracle[68723851392] = 2
        self.oracle[137443328000] = 4
        self.oracle[68723851265] = 3
        self.oracle[4466770362368] = 5
        self.oracle[70070059008] = 3
        self.oracle[70065897472] = 4
        self.oracle[71139606528] = 2
        self.oracle[70065864832] = 3
        self.oracle[138785341440] = 2
        self.oracle[70065864705] = 2
        self.oracle[4468112375808] = 3
        self.oracle[68740464768] = 2
        self.oracle[68732108928] = 3
        self.oracle[69000511616] = 3
        self.oracle[68732076416] = 3
        self.oracle[137451552896] = 3
        self.oracle[68732076161] = 3
        self.oracle[4466778587264] = 3
        self.oracle[8933804621824] = 4
        self.oracle[68740464641] = 3
        self.oracle[68732108801] = 3
        self.oracle[69000511489] = 3
        self.oracle[137451552769] = 3
        self.oracle[68732076035] = 3
        self.oracle[4466778587137] = 3
        self.oracle[4604213346304] = 3
        self.oracle[4604209184768] = 2
        self.oracle[4604477587456] = 3
        self.oracle[4604209152128] = 3
        self.oracle[4741648105472] = 3
        self.oracle[4604209152001] = 3
        self.oracle[13400302174208] = 5
        self.oracle[41943680] = 1
        self.oracle[25182848] = 3
        self.oracle[293601920] = 3
        self.oracle[25166976] = 3
        self.oracle[34384904832] = 3
        self.oracle[25166465] = 3
        self.oracle[4398071677568] = 3
        self.oracle[8406656] = 3
        self.oracle[4245120] = 2
        self.oracle[272647808] = 3
        self.oracle[4213376] = 2
        self.oracle[34363950720] = 2
        self.oracle[4212353] = 3
        self.oracle[4398050723456] = 1
        self.oracle[289407616] = 3
        self.oracle[281035392] = 3
        self.oracle[817889920] = 3
        self.oracle[281019520] = 3
        self.oracle[34640757376] = 5
        self.oracle[281019009] = 3
        self.oracle[4398327530112] = 3
        self.oracle[20972672] = 4
        self.oracle[12600448] = 1
        self.oracle[12585088] = 3
        self.oracle[34372322432] = 1
        self.oracle[12584065] = 4
        self.oracle[4398059095168] = 3
        self.oracle[34380710528] = 3
        self.oracle[34372338304] = 5
        self.oracle[103091798656] = 3
        self.oracle[34372321921] = 3
        self.oracle[4432418833024] = 3
        self.oracle[545260161] = 5
        self.oracle[541082241] = 3
        self.oracle[1077936769] = 5
        self.oracle[541066369] = 5
        self.oracle[34900804225] = 1
        self.oracle[541065859] = 5
        self.oracle[4398587576961] = 3
        self.oracle[4398067483264] = 3
        self.oracle[4398059111040] = 3
        self.oracle[4398059094657] = 3
        self.oracle[13194152116864] = 4
        self.oracle[88080385] = 4
        self.oracle[54542337] = 3
        self.oracle[322961409] = 3
        self.oracle[54526081] = 3
        self.oracle[34414264321] = 3
        self.oracle[54525955] = 4
        self.oracle[4398101037057] = 3
        self.oracle[46153729] = 3
        self.oracle[314572801] = 2
        self.oracle[46137473] = 4
        self.oracle[34405875713] = 2
        self.oracle[46137347] = 4
        self.oracle[4398092648449] = 2
        self.oracle[68794974209] = 4
        self.oracle[68761436161] = 3
        self.oracle[69029855233] = 4
        self.oracle[68761419905] = 4
        self.oracle[137480896513] = 4
        self.oracle[68761419779] = 4
        self.oracle[4466807930881] = 2
        self.oracle[42024961] = 2
        self.oracle[25313281] = 3
        self.oracle[293683201] = 2
        self.oracle[25247873] = 3
        self.oracle[34384986113] = 2
        self.oracle[25247747] = 3
        self.oracle[4398071758849] = 3
        self.oracle[360710145] = 4
        self.oracle[327172097] = 3
        self.oracle[864026625] = 3
        self.oracle[327155841] = 3
        self.oracle[34686894081] = 3
        self.oracle[327155715] = 3
        self.oracle[4398373666817] = 3
        self.oracle[92274817] = 3
        self.oracle[58736769] = 3
        self.oracle[58720641] = 3
        self.oracle[34418458753] = 3
        self.oracle[58720387] = 3
        self.oracle[4398105231489] = 3
        self.oracle[34452013057] = 3
        self.oracle[34418475009] = 3
        self.oracle[103137935361] = 3
        self.oracle[34418458627] = 3
        self.oracle[58720263] = 0
        self.oracle[92274691] = 4
        self.oracle[58736643] = 3
        self.oracle[4398105231363] = 3
        self.oracle[4398138785793] = 2
        self.oracle[37830657] = 2
        self.oracle[21118977] = 0
        self.oracle[289488897] = 4
        self.oracle[21053569] = 3
        self.oracle[34380791809] = 3
        self.oracle[21053443] = 2
        self.oracle[4398067564545] = 2
        self.oracle[46186497] = 2
        self.oracle[314589185] = 2
        self.oracle[46153857] = 3
        self.oracle[34405892097] = 3
        self.oracle[46153731] = 3
        self.oracle[4398092664833] = 2
        self.oracle[1379926017] = 3
        self.oracle[1363165185] = 2
        self.oracle[2436890625] = 3
        self.oracle[1363148929] = 3
        self.oracle[35722887169] = 4
        self.oracle[1363148803] = 3
        self.oracle[851443713] = 4
        self.oracle[314572929] = 4
        self.oracle[34674311169] = 4
        self.oracle[314572803] = 4
        self.oracle[37749377] = 1
        self.oracle[20988545] = 2
        self.oracle[289407617] = 4
        self.oracle[20972673] = 4
        self.oracle[34380710529] = 3
        self.oracle[20972163] = 3
        self.oracle[4398067483265] = 1
        self.oracle[46137729] = 4
        self.oracle[34405875841] = 3
        self.oracle[46137475] = 4
        self.oracle[4398092648577] = 2
        self.oracle[34447818753] = 5
        self.oracle[34414280705] = 2
        self.oracle[34682699777] = 4
        self.oracle[34414264449] = 1
        self.oracle[103133741057] = 5
        self.oracle[34414264323] = 3
        self.oracle[4432460775425] = 3
        self.oracle[103125352449] = 2
        self.oracle[34909192199] = 0
        self.oracle[34917580803] = 4
        self.oracle[34909208579] = 4
        self.oracle[35446063107] = 3
        self.oracle[34909192323] = 3
        self.oracle[103628668931] = 2
        self.oracle[4432955703299] = 3
        self.oracle[20971543] = 4
        self.oracle[12599319] = 3
        self.oracle[281018391] = 3
        self.oracle[12583063] = 3
        self.oracle[34372321303] = 3
        self.oracle[12582951] = 4
        self.oracle[4398059094039] = 4
        self.oracle[557842439] = 0
        self.oracle[574619651] = 2
        self.oracle[557858819] = 4
        self.oracle[1094713347] = 2
        self.oracle[557842563] = 5
        self.oracle[4398604353539] = 2
        self.oracle[4398092648451] = 2
        self.oracle[4399665528833] = 4
        self.oracle[4399661367297] = 2
        self.oracle[4400735076353] = 3
        self.oracle[4399661334657] = 3
        self.oracle[4434021072897] = 3
        self.oracle[4399661334531] = 3
        self.oracle[13195754356737] = 3
        self.oracle[4398604353665] = 4
        self.oracle[4398595981441] = 3
        self.oracle[4399132835969] = 3
        self.oracle[4398595965313] = 3
        self.oracle[4432955703425] = 3
        self.oracle[4398595965059] = 3
        self.oracle[13194688987265] = 3
        self.oracle[4432964091905] = 4
        self.oracle[4432955719681] = 3
        self.oracle[4433492574209] = 3
        self.oracle[4501675180033] = 3
        self.oracle[13229048725505] = 3
        self.oracle[35750016] = 2
        self.oracle[19038336] = 1
        self.oracle[287408256] = 1
        self.oracle[18973056] = 2
        self.oracle[34378711168] = 1
        self.oracle[18972801] = 3
        self.oracle[4398065483904] = 1
        self.oracle[44105856] = 2
        self.oracle[27394176] = 3
        self.oracle[295764096] = 3
        self.oracle[27328896] = 3
        self.oracle[34387067008] = 3
        self.oracle[27328641] = 3
        self.oracle[4398073839744] = 3
        self.oracle[34655469696] = 6
        self.oracle[4398342242432] = 5
        self.oracle[312508544] = 2
        self.oracle[832602240] = 3
        self.oracle[295731584] = 3
        self.oracle[295731329] = 3
        self.oracle[27296640] = 1
        self.oracle[44073344] = 0
        self.oracle[34387034496] = 3
        self.oracle[27296129] = 3
        self.oracle[4398073807232] = 3
        self.oracle[4432433545344] = 4
        self.oracle[34403811456] = 4
        self.oracle[103106510976] = 3
        self.oracle[34387034241] = 3
        self.oracle[44073089] = 1
        self.oracle[27295875] = 3
        self.oracle[4398073806977] = 3
        self.oracle[4398090584192] = 5
        self.oracle[13194166829184] = 3
        self.oracle[19071104] = 3
        self.oracle[10813568] = 3
        self.oracle[279117952] = 3
        self.oracle[10682752] = 3
        self.oracle[34370420864] = 3
        self.oracle[10682497] = 3
        self.oracle[4398057193600] = 3
        self.oracle[2425472] = 3
        self.oracle[590464] = 1
        self.oracle[268763776] = 4
        self.oracle[328832] = 3
        self.oracle[34360066688] = 3
        self.oracle[328321] = 1
        self.oracle[4398046839424] = 3
        self.oracle[270991488] = 3
        self.oracle[269156480] = 4
        self.oracle[805765248] = 3
        self.oracle[268894592] = 2
        self.oracle[34628632704] = 3
        self.oracle[268894337] = 2
        self.oracle[4398315405440] = 2
        self.oracle[459648] = 1
        self.oracle[2556288] = 3
        self.oracle[721280] = 3
        self.oracle[34360197504] = 2
        self.oracle[459137] = 3
        self.oracle[4398046970240] = 3
        self.oracle[34368323712] = 2
        self.oracle[34364260480] = 3
        self.oracle[34632564864] = 4
        self.oracle[34364129664] = 3
        self.oracle[103083606144] = 2
        self.oracle[34364129409] = 3
        self.oracle[4432410640512] = 2
        self.oracle[2556033] = 3
        self.oracle[721025] = 3
        self.oracle[34360197249] = 2
        self.oracle[458883] = 3
        self.oracle[4398046969985] = 3
        self.oracle[4398049067136] = 5
        self.oracle[4398047232128] = 3
        self.oracle[4432406708352] = 3
        self.oracle[13194139992192] = 3
        self.oracle[34638758016] = 6
        self.oracle[4398325530752] = 5
        self.oracle[279085184] = 1
        self.oracle[815890560] = 4
        self.oracle[279019904] = 3
        self.oracle[279019649] = 1
        self.oracle[270958720] = 3
        self.oracle[269123712] = 1
        self.oracle[805732480] = 4
        self.oracle[268861824] = 1
        self.oracle[34628599936] = 6
        self.oracle[268861569] = 4
        self.oracle[4398315372672] = 5
        self.oracle[2954985600] = 3
        self.oracle[2952953984] = 2
        self.oracle[5100372096] = 2
        self.oracle[2952888704] = 1
        self.oracle[37312626816] = 6
        self.oracle[2952888449] = 2
        self.oracle[4400999399552] = 2
        self.oracle[268796288] = 4
        self.oracle[34628534400] = 4
        self.oracle[268796033] = 4
        self.oracle[4398315307136] = 4
        self.oracle[18908544] = 3
        self.oracle[10552704] = 3
        self.oracle[278955392] = 3
        self.oracle[10520960] = 3
        self.oracle[34370258304] = 3
        self.oracle[10519937] = 1
        self.oracle[4398057031040] = 3
        self.oracle[2295168] = 3
        self.oracle[329088] = 2
        self.oracle[268633472] = 2
        self.oracle[199040] = 3
        self.oracle[34359936384] = 3
        self.oracle[198017] = 1
        self.oracle[4398046709120] = 3
        self.oracle[270632320] = 3
        self.oracle[268600704] = 2
        self.oracle[805406080] = 4
        self.oracle[268536192] = 2
        self.oracle[34628273536] = 2
        self.oracle[268535169] = 2
        self.oracle[4398315046272] = 2
        self.oracle[2197888] = 3
        self.oracle[166272] = 2
        self.oracle[102784] = 3
        self.oracle[34359839104] = 2
        self.oracle[100737] = 3
        self.oracle[4398046611840] = 3
        self.oracle[34361935232] = 2
        self.oracle[34359903616] = 2
        self.oracle[103079314816] = 2
        self.oracle[34359838081] = 2
        self.oracle[4432406349184] = 2
        self.oracle[165249] = 2
        self.oracle[2196865] = 3
        self.oracle[99715] = 2
        self.oracle[4398046610817] = 2
        self.oracle[4398054933888] = 2
        self.oracle[4398050772352] = 3
        self.oracle[4398319175040] = 2
        self.oracle[4398050740608] = 3
        self.oracle[4432410477952] = 3
        self.oracle[4398050739585] = 3
        self.oracle[13194143761792] = 3
        self.oracle[4432416833664] = 3
        self.oracle[34370388096] = 3
        self.oracle[34370322816] = 3
        self.oracle[103089799296] = 2
        self.oracle[34370322561] = 2
        self.oracle[34362261632] = 3
        self.oracle[34360426624] = 1
        self.oracle[34360164736] = 1
        self.oracle[103079641216] = 1
        self.oracle[34360164481] = 4
        self.oracle[4432406675584] = 4
        self.oracle[34360099200] = 1
        self.oracle[240518267520] = 5
        self.oracle[103081411200] = 2
        self.oracle[103079379584] = 2
        self.oracle[103347749504] = 3
        self.oracle[103079314560] = 2
        self.oracle[103079314049] = 2
        self.oracle[4501125825152] = 4
        self.oracle[34360098945] = 1
        self.oracle[4432678977664] = 3
        self.oracle[4432414736512] = 3
        self.oracle[4432410607744] = 3
        self.oracle[4432410542464] = 2
        self.oracle[4501130018944] = 2
        self.oracle[4432410542209] = 3
        self.oracle[13228503564416] = 2
        self.oracle[2457729] = 1
        self.oracle[426369] = 1
        self.oracle[2523265] = 3
        self.oracle[688257] = 1
        self.oracle[426115] = 3
        self.oracle[4398046937217] = 3
        self.oracle[360833] = 1
        self.oracle[360579] = 4
        self.oracle[4398046871681] = 4
        self.oracle[4398057160832] = 1
        self.oracle[4398057095552] = 2
        self.oracle[4398057095297] = 2
        self.oracle[13194150117504] = 2
        self.oracle[4398049034368] = 3
        self.oracle[4398047199360] = 1
        self.oracle[4398046937472] = 1
        self.oracle[13194139959424] = 3
        self.oracle[4398046871936] = 1
        self.oracle[13194139893888] = 4
        self.oracle[176177152] = 5
        self.oracle[109101056] = 3
        self.oracle[377503744] = 3
        self.oracle[109068416] = 1
        self.oracle[34468806656] = 2
        self.oracle[109068289] = 4
        self.oracle[4398155579392] = 3
        self.oracle[58834944] = 2
        self.oracle[92323840] = 0
        self.oracle[327204864] = 3
        self.oracle[58769536] = 3
        self.oracle[34418507776] = 2
        self.oracle[58769409] = 3
        self.oracle[360726528] = 2
        self.oracle[327172224] = 3
        self.oracle[92291200] = 2
        self.oracle[58737024] = 3
        self.oracle[34418475136] = 3
        self.oracle[34452029440] = 3
        self.oracle[103137951744] = 3
        self.oracle[42123264] = 3
        self.oracle[25477120] = 3
        self.oracle[293781504] = 3
        self.oracle[25346176] = 3
        self.oracle[34385084416] = 3
        self.oracle[25346049] = 2
        self.oracle[4398071857152] = 3
        self.oracle[21282816] = 3
        self.oracle[13156352] = 3
        self.oracle[281329664] = 3
        self.oracle[12894336] = 3
        self.oracle[34372632576] = 3
        self.oracle[12894209] = 3
        self.oracle[4398059405312] = 3
        self.oracle[289587200] = 3
        self.oracle[818069504] = 3
        self.oracle[281198720] = 3
        self.oracle[34640936960] = 3
        self.oracle[281198593] = 3
        self.oracle[4398327709696] = 3
        self.oracle[21151872] = 3
        self.oracle[12763520] = 3
        self.oracle[34372501632] = 3
        self.oracle[12763265] = 3
        self.oracle[4398059274368] = 3
        self.oracle[34380890112] = 3
        self.oracle[103091978240] = 3
        self.oracle[34372501505] = 3
        self.oracle[4432419012608] = 3
        self.oracle[21151745] = 2
        self.oracle[12763139] = 3
        self.oracle[4398059274241] = 3
        self.oracle[4398067662848] = 3
        self.oracle[13194152296448] = 3
        self.oracle[356532224] = 2
        self.oracle[323010560] = 2
        self.oracle[322977920] = 2
        self.oracle[322977793] = 3
        self.oracle[314621952] = 2
        self.oracle[314589312] = 3
        self.oracle[54575232] = 2
        self.oracle[88096896] = 2
        self.oracle[54542720] = 1
        self.oracle[34414280832] = 2
        self.oracle[54542465] = 2
        self.oracle[46186624] = 2
        self.oracle[46154112] = 1
        self.oracle[34405892224] = 2
        self.oracle[34447835136] = 3
        self.oracle[34414313472] = 2
        self.oracle[103133757440] = 5
        self.oracle[4432460791808] = 2
        self.oracle[34405924864] = 2
        self.oracle[103125368832] = 5
        self.oracle[153124864] = 2
        self.oracle[86048768] = 2
        self.oracle[354451456] = 2
        self.oracle[86016128] = 2
        self.oracle[34445754368] = 2
        self.oracle[86016001] = 2
        self.oracle[4398132527104] = 5
        self.oracle[589316224] = 0
        self.oracle[589316097] = 1
        self.oracle[589348864] = 2
        self.oracle[1126187008] = 4
        self.oracle[34949054464] = 4
        self.oracle[4398635827200] = 4
        self.oracle[52494464] = 2
        self.oracle[52461952] = 1
        self.oracle[34412200064] = 2
        self.oracle[52461697] = 2
        self.oracle[4398098972800] = 2
        self.oracle[52494337] = 2
        self.oracle[34412199937] = 3
        self.oracle[52461571] = 5
        self.oracle[4398098972673] = 2
        self.oracle[555761794] = 4
        self.oracle[547405954] = 2
        self.oracle[1084244098] = 3
        self.oracle[547373442] = 3
        self.oracle[34907111554] = 1
        self.oracle[547373188] = 3
        self.oracle[4398593884290] = 1
        self.oracle[555761921] = 4
        self.oracle[547406081] = 2
        self.oracle[1084244225] = 3
        self.oracle[547373569] = 3
        self.oracle[34907111681] = 3
        self.oracle[547373315] = 3
        self.oracle[4398593884417] = 4
        self.oracle[1629503616] = 0
        self.oracle[1629503489] = 1
        self.oracle[1646280704] = 2
        self.oracle[1629536256] = 2
        self.oracle[2703245312] = 2
        self.oracle[4399676014592] = 2
        self.oracle[547537024] = 0
        self.oracle[547536897] = 1
        self.oracle[555925504] = 4
        self.oracle[547667968] = 3
        self.oracle[1084407808] = 3
        self.oracle[34907275264] = 3
        self.oracle[4398594048000] = 3
        self.oracle[1101021312] = 0
        self.oracle[1101021185] = 1
        self.oracle[1117798400] = 3
        self.oracle[1101053952] = 3
        self.oracle[2174763008] = 3
        self.oracle[4399147532288] = 3
        self.oracle[4399667626112] = 0
        self.oracle[4399667625985] = 1
        self.oracle[4399667658752] = 4
        self.oracle[4400741367808] = 2
        self.oracle[13195760648192] = 4
        self.oracle[295715073] = 5
        self.oracle[34387017985] = 4
        self.oracle[44056833] = 3
        self.oracle[27312385] = 3
        self.oracle[27279873] = 3
        self.oracle[27279619] = 3
        self.oracle[4398073790721] = 3
        self.oracle[77627393] = 2
        self.oracle[44105729] = 2
        self.oracle[312508417] = 2
        self.oracle[34403811329] = 2
        self.oracle[44072963] = 3
        self.oracle[4398090584065] = 2
        self.oracle[362807297] = 5
        self.oracle[34454110209] = 4
        self.oracle[94371843] = 4
        self.oracle[4398140882945] = 1

        return
