
class Board:

    
    def __init__(self, board_str):

        self.board = self.create_board(board_str)

        return

    
    def create_board(self, board_str):

        board = []
        rows = board_str.split(",")

        for row_str in rows:

            row = list(row_str)
            board.append(row)

        return board

    def __str__(self):

        ret = "\n---------------\n"

        for i in range(len(self.board)):

            for char in self.board[len(self.board) - i - 1]:

                ret += ' ' + char

            ret += '\n'

        ret += "\n---------------\n"

        return ret




class State:

    def __init__(self, board_str):

        self.board = Board(board_str)
        self.evaluation = None

        return

