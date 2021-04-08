
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


    def utility(state):

        # TODO

        # if red is winner, return 10000
        # if yellow is winner, return -10000

        return


    def evaluation(state):

        # TODO

        # eval = score(state, red player) - score(state, yellow player)
        # return eval


        return


    def score(state, player):

        # TODO

        # score = number of player tokens
        # score += 10 * num_in_a_row(2, state, player)
        # score += 100 * num_in_a_row(3, state, player)
        # score += 1000 * num_in_a_row(4 or more, state, player)
        # return score

        return


    def num_in_a_row(count, state, player):

        # return the number of times there exists count-in-a-row for player in state

        return