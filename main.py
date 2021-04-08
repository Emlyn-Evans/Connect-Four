
import sys
from state_class import Board, State



def print_arguments():

    board_str = sys.argv[1]
    player_turn = sys.argv[2]
    algorithm = sys.argv[3]
    max_depth = int(sys.argv[4])

    print(f"Board: {board_str}")
    print(f"Player turn: {player_turn}")
    print(f"Algorithm type: {algorithm}")
    print(f"Max depth of search: {max_depth}")

    return

def get_board_str():

    return sys.argv[1]



def create_state():

    board_str = get_board_str()
    state = State(board_str)

    print(state.board)
    
    return


create_state()

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