# Plays a simple tic tac toe game with ai.
# Computer = 1's, player = 2's
# Currently no functionality.

# Packages

import numpy as np

# Variables

board = np.zeros((3,3), dtype=ch)
round = 0
player_turn = False
game_over = False

# Directions to player

print("CPU is 1's, Player is 2's.")
firstturntext = "Your turn. (Format: row, column. Ex: middle square is '2,2')"
turntext = "Your turn."
losetext = "Game over (lose)"
tietext = "Game over (tie)"

# Functions

def get_move(board):
    if round == 0:
        raw_move = input(firstturntext)
    else: raw_move = input(turntext)
    move = input_to_tuple(raw_move)
    return = check_board(move)

def input_to_tuple(raw_move):
    pass

def check_board(move):
    pass

def cpu_move(board):
    pass



while(player-turn == True):
    if get_move(board) == True:
        # do move
        player-turn = False
        cpu_move(board)



print(board)