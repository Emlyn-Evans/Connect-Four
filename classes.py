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

            if key not in self.oracle:

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
                        self.oracle[self.board.get_key()] = opt_col

            looping = False

            if self.board.moves_player >= move_depth:

                return

            play_col = self.oracle[self.board.get_key()]

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

    def read_oracle(self):

        # Optimal moves for 3-4 moves each
        self.oracle[0] = 3
        self.oracle[8388608] = 3
        self.oracle[41943040] = 3
        self.oracle[25182208] = 3
        self.oracle[293601280] = 3
        self.oracle[25165952] = 3
        self.oracle[34384904192] = 3
        self.oracle[25165825] = 4
        self.oracle[4398071676928] = 2
        self.oracle[4210688] = 5
        self.oracle[68727881728] = 3
        self.oracle[68723720192] = 2
        self.oracle[68992122880] = 4
        self.oracle[68723687552] = 3
        self.oracle[137443164160] = 6
        self.oracle[68723687425] = 3
        self.oracle[4466770198528] = 5
        self.oracle[272629760] = 1
        self.oracle[276824320] = 3
        self.oracle[272646400] = 2
        self.oracle[809500928] = 4
        self.oracle[272630272] = 0
        self.oracle[34632368384] = 3
        self.oracle[272630017] = 1
        self.oracle[4398319141120] = 3
        self.oracle[4194432] = 1
        self.oracle[8389248] = 3
        self.oracle[4211328] = 1
        self.oracle[272630400] = 3
        self.oracle[4195456] = 3
        self.oracle[34363933312] = 3
        self.oracle[4194945] = 4
        self.oracle[4398050706048] = 3
        self.oracle[34363932672] = 1
        self.oracle[34368127232] = 2
        self.oracle[34363949312] = 1
        self.oracle[34363933184] = 2
        self.oracle[103083409664] = 2
        self.oracle[34363932929] = 3
        self.oracle[4432410444032] = 2
        self.oracle[4194305] = 3
        self.oracle[20971521] = 3
        self.oracle[12599297] = 3
        self.oracle[281018369] = 3
        self.oracle[12583041] = 3
        self.oracle[34372321281] = 3
        self.oracle[12582915] = 3
        self.oracle[4398059094017] = 3
        self.oracle[4398050705408] = 3
        self.oracle[4398067482624] = 3
        self.oracle[4398059110400] = 3
        self.oracle[4398327529472] = 3
        self.oracle[4398059094144] = 3
        self.oracle[4432418832384] = 3
        self.oracle[13194152116224] = 3
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
        self.oracle[4398327529473] = 3
        self.oracle[4194433] = 3
        self.oracle[20971649] = 2
        self.oracle[12583297] = 3
        self.oracle[34372321409] = 3
        self.oracle[12583043] = 3
        self.oracle[4398059094145] = 3
        self.oracle[34363932673] = 3
        self.oracle[34380709889] = 3
        self.oracle[103091798017] = 3
        self.oracle[34372321283] = 4
        self.oracle[4432418832385] = 3
        self.oracle[4194307] = 3
        self.oracle[12582919] = 0
        self.oracle[20971523] = 4
        self.oracle[4398059094019] = 3
        self.oracle[4398050705409] = 2
        self.oracle[4398054932481] = 4
        self.oracle[4398050770945] = 4
        self.oracle[4398319173633] = 2
        self.oracle[4398050738305] = 3
        self.oracle[4432410476545] = 3
        self.oracle[4398050738179] = 4
        self.oracle[13194143760385] = 4
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
        self.oracle[4398071693312] = 3
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
        self.oracle[817905664] = 3
        self.oracle[281034880] = 3
        self.oracle[34640773120] = 3
        self.oracle[4398327545856] = 3
        self.oracle[4210816] = 3
        self.oracle[20988032] = 3
        self.oracle[12632192] = 3
        self.oracle[12599680] = 3
        self.oracle[34372337792] = 3
        self.oracle[4398059110528] = 3
        self.oracle[34363949056] = 3
        self.oracle[34380726272] = 3
        self.oracle[34372370432] = 3
        self.oracle[103091814400] = 3
        self.oracle[4432418848768] = 3
        self.oracle[4398050721792] = 3
        self.oracle[4398067499008] = 2
        self.oracle[4398059143168] = 3
        self.oracle[13194152132608] = 3
        self.oracle[2097152] = 3
        self.oracle[18874368] = 3
        self.oracle[85983232] = 2
        self.oracle[52445184] = 1
        self.oracle[320864256] = 2
        self.oracle[52428928] = 2
        self.oracle[34412167168] = 4
        self.oracle[52428801] = 3
        self.oracle[4398098939904] = 3
        self.oracle[10502144] = 4
        self.oracle[547373184] = 0
        self.oracle[547373057] = 1
        self.oracle[555761664] = 4
        self.oracle[547405824] = 2
        self.oracle[1084243968] = 3
        self.oracle[34907111424] = 3
        self.oracle[4398593884160] = 4
        self.oracle[278921216] = 2
        self.oracle[34638692352] = 6
        self.oracle[4398325465088] = 5
        self.oracle[287342592] = 2
        self.oracle[278986752] = 3
        self.oracle[815824896] = 4
        self.oracle[278953985] = 2
        self.oracle[10485888] = 2
        self.oracle[34370224128] = 4
        self.oracle[34915483648] = 4
        self.oracle[35443965952] = 3
        self.oracle[34907095168] = 3
        self.oracle[103626571776] = 3
        self.oracle[34907095041] = 3
        self.oracle[4432953606144] = 3
        self.oracle[10485761] = 3
        self.oracle[27279361] = 1
        self.oracle[27263105] = 2
        self.oracle[44040193] = 2
        self.oracle[295698433] = 3
        self.oracle[34387001345] = 3
        self.oracle[27262979] = 3
        self.oracle[4398073774081] = 3
        self.oracle[4398056996864] = 3
        self.oracle[4398342209536] = 5
        self.oracle[4432433512448] = 4
        self.oracle[4398090551296] = 4
        self.oracle[4398073790464] = 3
        self.oracle[4398073774208] = 3
        self.oracle[13194166796288] = 3
        self.oracle[268435456] = 3
        self.oracle[276824064] = 3
        self.oracle[310378496] = 3
        self.oracle[830472192] = 3
        self.oracle[293601408] = 3
        self.oracle[34653339648] = 3
        self.oracle[4398340112384] = 4
        self.oracle[809500672] = 4
        self.oracle[2961178624] = 3
        self.oracle[2957000704] = 3
        self.oracle[5104467968] = 3
        self.oracle[2956984448] = 3
        self.oracle[37316722688] = 3
        self.oracle[2956984321] = 3
        self.oracle[4401003495424] = 3
        self.oracle[272629888] = 3
        self.oracle[289407104] = 3
        self.oracle[817889408] = 3
        self.oracle[281018752] = 3
        self.oracle[34640756864] = 3
        self.oracle[4398327529600] = 3
        self.oracle[34632368128] = 3
        self.oracle[4432687267840] = 3
        self.oracle[34649145344] = 3
        self.oracle[35177627648] = 3
        self.oracle[103360233472] = 3
        self.oracle[4398319140864] = 3
        self.oracle[4398335918080] = 4
        self.oracle[4398864400384] = 3
        self.oracle[13194420551680] = 3
        self.oracle[34359738368] = 4
        self.oracle[34898706432] = 3
        self.oracle[34896625664] = 4
        self.oracle[35972464640] = 3
        self.oracle[35970400256] = 2
        self.oracle[37044109312] = 2
        self.oracle[35970367616] = 2
        self.oracle[104689844224] = 4
        self.oracle[35970367489] = 2
        self.oracle[4434016878592] = 2
        self.oracle[35433480192] = 4
        self.oracle[37583060992] = 3
        self.oracle[37580980224] = 4
        self.oracle[39728447488] = 5
        self.oracle[37580963968] = 3
        self.oracle[106300440576] = 4
        self.oracle[37580963841] = 4
        self.oracle[4435627474944] = 4
        self.oracle[34896609408] = 4
        self.oracle[35972448384] = 3
        self.oracle[37044093056] = 4
        self.oracle[35970351488] = 1
        self.oracle[104689827968] = 4
        self.oracle[35970351233] = 3
        self.oracle[4434016862336] = 4
        self.oracle[103616086016] = 5
        self.oracle[378496090112] = 3
        self.oracle[378494009344] = 4
        self.oracle[379030863872] = 4
        self.oracle[378493993088] = 2
        self.oracle[653371899904] = 4
        self.oracle[378493992961] = 3
        self.oracle[4776540504064] = 4
        self.oracle[34896609281] = 4
        self.oracle[35972448257] = 3
        self.oracle[37044092929] = 4
        self.oracle[104689827841] = 4
        self.oracle[35970351107] = 2
        self.oracle[4434016862209] = 2
        self.oracle[4432943120384] = 4
        self.oracle[4434018959360] = 4
        self.oracle[4435090604032] = 4
        self.oracle[4502736338944] = 4
        self.oracle[13230109884416] = 4
        self.oracle[4398046511104] = 3
        self.oracle[4398054899712] = 3
        self.oracle[4398088454144] = 1
        self.oracle[4398071677056] = 3
        self.oracle[4432431415296] = 3
        self.oracle[13194164699136] = 3
        self.oracle[4398050705536] = 3
        self.oracle[4398067482752] = 3
        self.oracle[4398059094400] = 3
        self.oracle[4432418832512] = 3
        self.oracle[13194152116352] = 2
        self.oracle[4432410443776] = 3
        self.oracle[4432427220992] = 5
        self.oracle[4501138309120] = 3
        self.oracle[13228511854592] = 3
        self.oracle[13194143727616] = 3
        self.oracle[30786338160640] = 6
        self.oracle[13194160504832] = 2
        self.oracle[13194152116225] = 3
        self.oracle[176160768] = 2
        self.oracle[109068288] = 2
        self.oracle[377487360] = 4
        self.oracle[109052032] = 1
        self.oracle[34468790272] = 5
        self.oracle[109051905] = 2
        self.oracle[4398155563008] = 2
        self.oracle[92291072] = 2
        self.oracle[58769408] = 3
        self.oracle[327172096] = 3
        self.oracle[58736768] = 3
        self.oracle[34418475008] = 3
        self.oracle[58736641] = 3
        self.oracle[4398105247744] = 3
        self.oracle[360710144] = 4
        self.oracle[864026624] = 3
        self.oracle[327155840] = 3
        self.oracle[34686894080] = 3
        self.oracle[327155713] = 3
        self.oracle[4398373666816] = 3
        self.oracle[92274816] = 1
        self.oracle[58720640] = 3
        self.oracle[34418458752] = 3
        self.oracle[58720385] = 3
        self.oracle[4398105231488] = 3
        self.oracle[34452013056] = 5
        self.oracle[103137935360] = 3
        self.oracle[34418458625] = 3
        self.oracle[4432464969728] = 3
        self.oracle[578813953] = 2
        self.oracle[562053121] = 3
        self.oracle[1098907649] = 2
        self.oracle[562036865] = 5
        self.oracle[34921775105] = 3
        self.oracle[562036739] = 2
        self.oracle[4398608547841] = 2
        self.oracle[4398088486912] = 4
        self.oracle[4398071742464] = 4
        self.oracle[4398340145152] = 3
        self.oracle[4398071709824] = 3
        self.oracle[4432431448064] = 1
        self.oracle[4398071709697] = 4
        self.oracle[13194164731904] = 4
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
        self.oracle[310378752] = 0
        self.oracle[293617920] = 3
        self.oracle[830472448] = 1
        self.oracle[293601792] = 3
        self.oracle[34653339904] = 3
        self.oracle[293601537] = 3
        self.oracle[4398340112640] = 3
        self.oracle[276906240] = 3
        self.oracle[272777472] = 4
        self.oracle[809582848] = 2
        self.oracle[272712192] = 2
        self.oracle[34632450304] = 3
        self.oracle[272711937] = 3
        self.oracle[4398319223040] = 4
        self.oracle[2961178880] = 3
        self.oracle[2957000960] = 2
        self.oracle[5104468224] = 3
        self.oracle[2956984832] = 2
        self.oracle[37316722944] = 4
        self.oracle[2956984577] = 1
        self.oracle[4401003495680] = 3
        self.oracle[272646658] = 2
        self.oracle[4432687268096] = 3
        self.oracle[34649145600] = 4
        self.oracle[34640773376] = 3
        self.oracle[35177627904] = 3
        self.oracle[34640757248] = 3
        self.oracle[103360233728] = 3
        self.oracle[34640756993] = 3
        self.oracle[276824833] = 3
        self.oracle[272646913] = 3
        self.oracle[809501441] = 4
        self.oracle[272631041] = 3
        self.oracle[34632368897] = 3
        self.oracle[272630531] = 1
        self.oracle[4398319141633] = 3
        self.oracle[4398335918336] = 3
        self.oracle[4398327546112] = 3
        self.oracle[4398864400640] = 3
        self.oracle[4398327529984] = 3
        self.oracle[4398327529729] = 3
        self.oracle[13194420551936] = 3
        self.oracle[176226304] = 4
        self.oracle[444628992] = 4
        self.oracle[1518403584] = 2
        self.oracle[2592112640] = 2
        self.oracle[1518370944] = 4
        self.oracle[35878109184] = 2
        self.oracle[1518370817] = 2
        self.oracle[4399564881920] = 4
        self.oracle[176193664] = 5
        self.oracle[69164105856] = 4
        self.oracle[34535931904] = 1
        self.oracle[176193537] = 4
        self.oracle[4398222704640] = 4
        self.oracle[176242688] = 2
        self.oracle[176504832] = 1
        self.oracle[444809216] = 2
        self.oracle[176373888] = 2
        self.oracle[34536112128] = 2
        self.oracle[176373761] = 2
        self.oracle[4398222884864] = 2
        self.oracle[109199360] = 2
        self.oracle[377896960] = 2
        self.oracle[109461505] = 3
        self.oracle[176570368] = 5
        self.oracle[109723648] = 5
        self.oracle[109461632] = 5
        self.oracle[34469199872] = 2
        self.oracle[4398155972608] = 0
        self.oracle[377569280] = 2
        self.oracle[377831424] = 3
        self.oracle[914571264] = 2
        self.oracle[377700480] = 3
        self.oracle[34737438720] = 5
        self.oracle[377700353] = 4
        self.oracle[4398424211456] = 4
        self.oracle[109133952] = 2
        self.oracle[109396096] = 3
        self.oracle[109265280] = 2
        self.oracle[34469003392] = 3
        self.oracle[109265025] = 2
        self.oracle[4398155776128] = 2
        self.oracle[34468872192] = 2
        self.oracle[34469134336] = 3
        self.oracle[103188480000] = 2
        self.oracle[34469003265] = 5
        self.oracle[4432515514368] = 5
        self.oracle[109133825] = 2
        self.oracle[109395969] = 3
        self.oracle[109264899] = 2
        self.oracle[4398155776001] = 2
        self.oracle[4398155644928] = 2
        self.oracle[4398155907072] = 1
        self.oracle[13194248798208] = 2

        return
