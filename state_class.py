
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

                if char == 'r':

                    row.append('X')

                elif char == 'y':

                    row.append('O')

                else:

                    row.append('.')

            board.append(row)

        return board

    def compute_filled_cols(self):

        cols = [0, 0, 0, 0, 0, 0, 0]

        for row in self.board:

            for col in range(len(row)):

                if row[col] != '.':

                    cols[col] += 1

        return cols

    def add_move(self, col, char):

        if self.filled_cols[col] < 6:

            self.board[self.filled_cols[col]][col] = char
            self.filled_cols[col] += 1

        else:

            print("INVALID MOVE")

        return


    def __str__(self):

        ret = "\n---------------\n"

        for i in range(len(self.board)):

            for char in self.board[len(self.board) - i - 1]:

                ret += ' ' + char

            ret += '\n'

        ret += "\n---------------\n"

        return ret

    def get_filled_cols(self):

        return self.filled_cols




class State:

    def __init__(self, board_str):

        self.board = Board(board_str)
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

        # return the number of times there exists count-in-a-row for player in state

        return