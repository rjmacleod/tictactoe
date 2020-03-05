# Plays a simple tic tac toe game with ai.
# Computer = 1's, player = 2's
# CPU currently always goes first and will always win/tie

# Packages

import numpy as np
import math
from random import random
import operator

# Variables and Constants ##########################################

board = np.zeros((3,3), dtype=int)
first_move = True
player_turn = False
rot_index = 0



# Game not over: 0
# CPU win: 1
# Player win: 2
# Tie: 3
win_state = 0

# Board shortcuts
corners = [[0,0],[2,0],[2,2],[0,2]]
diagonal_1 = [[0,0],[1,1],[2,2]]
diagonal_2 = [[0,2],[1,1],[2,0]]
numboard = np.array([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]])
id_board = np.reshape(np.arange(9),(3,3))


# Directions to player

starttext = "CPU is 1's, Player is 2's."
turntext = "Your turn: "
cpumovetext = "CPU plays at: "
usagetext = "Format: row,column. Ex: middle cell is '2,2'"
losetext = "Game over (lose)"
tietext = "Game over (tie)"
wintext = "Win???"

# Functions ###############################

def check_in_array(master, check):
    for item in master:
        if np.array_equal(item, check):
            return True
    return False

def get_valid_move(board):
    while True:
        raw_move = input(turntext)
        move = input_to_tuple(raw_move)
        if check_valid_move(move,board):
            return move
        else:
            print(usagetext)
            print(board)

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

# The CPU ai likes having the board with the first move in the top left corner
def rotate_board(board, rot_index):
    if rot_index > 0:
        return np.rot90(board,rot_index)
    else: return board

def reverse_rotate_board(board, rot_index):
    if rot_index > 0:
        return np.rot90(board, 4 - rot_index)
    else: return board

# It looks weird, but this translates a board coordinate from the "real" coords to the ai-friendly rotated coords
def rotate_move(move, rot_index):
    print("rot index is ", rot_index)
    if rot_index > 0:
        index = -1
        print("move is",move)
        for i in range(9):
            if np.array_equal(numboard[i],move):
                index = i
                print("index is ", index)
        temp_id_board = np.rot90(id_board)
        i = 0
        for row in temp_id_board:
            j = 0
            for cell in row:
                if cell == index:
                    return [i,j]
                j += 1
            i += 1
    else: return move

# First move is always a random corner
def generate_first_move(board):
    global rot_index
    rot_index = math.floor(random()*4)
    return corners[rot_index]

# BIG Function that will analyze board and choose a move randomly from a list of "good" moves
def generate_move(board,game,rot_index):
    turn = turnData()

    if game.round == 2:
        analyze_first_player_move(game,rot_index)
        return game.second_move

    # First we check for the winning move
    turn.CPU_crit = check_if_critical(board,turn, 1)
    if not np.array_equal(turn.CPU_crit, [-1,-1]):
        return turn.CPU_crit
    
    # then we block the player's winning move
    turn.player_crit = check_if_critical(board,turn, 2)
    if not np.array_equal(turn.player_crit, [-1,-1]):
        return turn.player_crit

    # then we check for semi-critical corners
    semi_crit_check(turn)
    if not np.array_equal(turn.semi_crit, [-1,-1]):
        return turn.semi_crit

    # if all fails, give a random space
    while(True):
        r = math.floor(random()*9)
        if check_valid_move(numboard[r],board):
            return numboard[r]


def check_if_critical(board,turn,id):
    # id is int, id = 1 (CPU) or 2 (Player)
    # goes thru all rows and returns [-1,-1] if there is no "winning" move for the player id,
    # returns the "winning" move if it exists,
    # or returns [-2,-2] if player id has won.

    result = [-1,-1]

    # ROWS
    i = 0
    for row in board:
        # x is CPU count, y is player count, z is open space count
        # count = (x,y,z)
        count = countData()
        j = 0
        for cell in row:
            if analyze_space(cell,count):
                if cell == 0 and check_in_array(corners,[i,j]):
                    count.semi_crit_corner = [i,j]
                count.crit_zero_space = [i,j]
            j += 1
        analyze_count(count,turn)
        if count.is_crit > 0 and count.is_crit == id and not np.array_equal(result, [-2,-2]):
            return count.crit_zero_space
        elif count.win_state == id:
            result = [-2,-2]
        i += 1

    # COLUMNS
    i = 0
    for column in board.T:
        count = countData()
        j = 0
        for cell in column:
            if analyze_space(cell,count):
                count.crit_zero_space = [i,j]
            j += 1
        analyze_count(count,turn)
        if count.is_crit > 0 and count.is_crit == id and not np.array_equal(result, [-2,-2]):
            return count.crit_zero_space
        elif count.win_state == id:
            result = [-2,-2]
        i += 1

    # DIAGONALS

    diagonal_1_cells = [board[0][0], board[1][1], board[2][2]]
    diagonal_2_cells = [board[2][0], board[1][1], board[0][2]]
    
    count = countData()
    i = 0
    for cell in diagonal_1_cells:
        if analyze_space(cell,count):
            count.crit_zero_space = diagonal_1[i]
        i += 1
    analyze_count(count,turn)
    if count.is_crit > 0 and count.is_crit == id and not np.array_equal(result, [-2,-2]):
        return count.crit_zero_space
    elif count.win_state == id:
        result = [-2,-2]

    count = countData()
    i = 0
    for cell in diagonal_2_cells:
        if analyze_space(cell,count):
            count.crit_zero_space = diagonal_2[i]
        i += 1
    analyze_count(count,turn)
    if count.is_crit > 0 and count.is_crit == id and not np.array_equal(result, [-2,-2]):
        count.crit_zero_space
    elif count.win_state == id:
        result = [-2,-2]

    return result


def analyze_space(cell, count):
    # x is CPU count, y is player count, z is open space count
    # count.data = [x,y,z]
    # return True if space is open
    if cell == 1:
        count.data[0] += 1
        return False
    elif cell == 2:
        count.data[1] += 1
        return False
    elif cell == 0:
        count.data[2] += 1
        return True

# This function takes an object of the countData class, looks at it, and interprets
# into is_crit (1 if CPU has critical move, 2 if player has critical move) and
# win_state (0 for game on, 1 for CPU win, 2 for player win)
def analyze_count(count,turn):
    if np.array_equal(count.data,[2,0,1]):
        count.is_crit = 1
    elif np.array_equal(count.data, [0,2,1]):
        count.is_crit = 2
    elif np.array_equal(count.data, [3,0,0]):
        count.win_state = 1
    elif np.array_equal(count.data, [0,3,0]):
        count.win_state = 2
    elif np.array_equal(count.data, [1,0,2]):
        i = 0
        for item in numboard:
            if np.array_equal(count.semi_crit_corner,item):
                turn.corner_crit_count[i] += 1
            i += 1

def semi_crit_check(turn):
    for corner in turn.corner_crit_count:
        if turn.corner_crit_count[corner] > 1:
            turn.semi_crit = numboard[corner]

def choose_move(move1,move2):
    if random() > 0.5:
        return move1
    else: return move2

def analyze_first_player_move(game,rot_index):
    fm = rotate_move(game.player_moves[0], rot_index)

    if np.array_equal(fm,[1,0]):
        game.pattern = 1.1
        game.second_move = [0,2]
    elif np.array_equal(fm,[0,1]):
        game.pattern = 1.2
        game.second_move = [2,0]
    elif np.array_equal(fm,[2,0]):
        game.pattern = 2.1
        game.second_move = [0,2]
    elif np.array_equal(fm,[0,2]):
        game.pattern = 2.2
        game.second_move = [2,0]
    elif np.array_equal(fm,[1,1]):
        game.pattern = 3.1
        print(game.pattern)
        game.second_move = choose_move([2,0],[0,2])
    elif np.array_equal(fm,[2,2]):
        game.pattern = 3.2
        print(game.pattern)
        game.second_move = choose_move([2,0],[0,2])
    elif np.array_equal(fm,[2,1]):
        game.pattern = 4.1
        game.second_move = [2,0]
    elif np.array_equal(fm,[1,2]):
        game.pattern = 4.2
        game.second_move = [0,2]



# Actually execute a generated move
def execute_cpu_move(move,board):
    board[move[0]][move[1]] = 1
    print(cpumovetext, move[0] + 1,',', move[1] + 1)

class countData:
    def __init__(self):
        self.data = [0,0,0]
        self.is_crit = 0
        self.win_state = 0
        self.crit_zero_space = [-1,-1]
        self.semi_crit_corner = [-1,-1]

class turnData:
    def __init__(self):
        self.CPU_crit = [-1,-1]
        self.player_crit = [-1,-1]
        self.corner_crit_count = {}
        self.semi_crit = [-1,-1]
        for i in range(9):
            self.corner_crit_count[i] = 0


class gameData:
    def __init__(self, first_move):
        self.first_move = first_move
        self.player_moves = []
        self.round = 1
        self.pattern = 0
        self.second_move = [-1,-1]

    def get_last_player_move(self):
        return rotate_move(player_moves[self.round - 2], rot_index)

        



# START UP #############################

print(starttext)
# initialize the object holding our game data
first_cpu_move = generate_first_move(board)
print(rot_index)
game = gameData(first_cpu_move)
execute_cpu_move(game.first_move,board)
print(board)


# MAIN GAME LOOP #########################

while(win_state == 0):
    # if we have a valid player input:
    player_move = get_valid_move(board)
    game.player_moves.append(player_move)
    # execute move
    board[player_move[0]][player_move[1]] = 2
    # update board
    print(board)
    # see if game is over
    # check_if_critical returns [-2,-2] if game is won
    turn = turnData()
    if np.array_equal(check_if_critical(board,turn,2),[-2,-2]):
        win_state = 2
    # otherwise, CPU turn

    game.round += 1

    # UNCOMMENT THESE WHEN CPU AI IS READY ####
    alt_board = rotate_board(board,rot_index)
    cpu_move = generate_move(alt_board,game,rot_index)
    execute_cpu_move(cpu_move,alt_board)
    reverse_rotate_board(alt_board,rot_index)
    turn = turnData()

    if np.array_equal(check_if_critical(board,turn,1),[-2,-2]):
        win_state = 1
    print(game.round)
    print(board)

if win_state == 1:
    print(losetext)
elif win_state == 2:
    print(wintext)
elif win_state == 3:
    print(tietext)