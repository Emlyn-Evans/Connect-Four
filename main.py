
import sys

board_str = sys.argv[1]
player_turn = sys.argv[2]
algorithm = sys.argv[3]
max_depth = int(sys.argv[4])

print(f"Board: {board_str}")
print(f"Player turn: {player_turn}")
print(f"Algorithm type: {algorithm}")
print(f"Max depth of search: {max_depth}")
