# Plays a simple tic tac toe game with ai.
# Computer = 1's, player = 2's
# Currently no functionality.

# Packages

import numpy as np
import math
from random import random

# Variables

board = np.zeros((3,3), dtype=int)
first_move = True
player_turn = False

# Game not over: 0
# CPU win: 1
# Player win: 2
win_state = 0

# Board shortcuts
corners = [[0,0],[2,0],[0,2],[2,2]]

# Directions to player

starttext = "CPU is 1's, Player is 2's."
turntext = "Your turn: "
usagetext = "Format: row,column. Ex: middle cell is '2,2'"
losetext = "Game over (lose)"
tietext = "Game over (tie)"
wintext = "Win???"

# Functions

def get_valid_move(board):
    while True:
        raw_move = input(turntext)
        move = input_to_tuple(raw_move)
        if check_valid_move(move,board):
            return move
        else:
            print(usagetext)

def input_to_tuple(raw_move):
    # output set to (-1,-1) or 'bad move' by default
    output = [-1,-1]

    # x is an intermediary, list of input broken by ','
    x = raw_move.split(',')
    print(x)
    # if we have more then 2 items in x, bad input
    try:
        if len(x) != 2:
            print("Bad coordinates.")
            return output
    except:
        print("Generic input error")
        return output

    # iterate through the cells
    for cell in range(2):
        x[cell] = int(x[cell])
        if x[cell] > 3 or x[cell] < 1:
            print("Input out of cell range.")
            return output
        # player input is 1-3 but board index 0-2
        output[cell] = x[cell] - 1

    return output

# checks for 'bad move' AND if cell is empty
def check_valid_move(move, board):
    for cell in range(2):
        if move[cell] == -1:
            return False
    if board[move[0]][move[1]] == 0:
        return True
    return False

def generate_first_move(board):
    index = 1 + math.floor(random()*4)
    return corners[index]

def generate_move(board):
    pass

def cpu_move(move,board):
    pass

def check_win_cond(board):
    # iterates thru rows / then columns:
    # TO DO: DIAGONAL CHECK
    # returns 0 if no win, 1 if CPU win, 2 if player win
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] == 1:
                return 1
            elif row[0] == 2:
                return 2
    for i in range(2):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == 1:
                return 1
            elif board[0][i] == 2:
                return 2
    return 0

# START UP
print(starttext)
generate_first_move(board)
cpu_move(board)


# MAIN GAME LOOP

while(win_state == 0):
    # if we have a valid player input:
    move = get_valid_move(board)
    # execute move
    board[move[0]][move[1]] = 2
    # update board
    print(board)
    # see if game is over
    win_state = check_win_cond(board)
    # otherwise, CPU turn
    generate_move(board)
    cpu_move(move,board)
    win_state = check_win_cond(board)
    print(win_state)
    print(board)
        



print(board)