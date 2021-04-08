
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