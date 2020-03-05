# trying again from scratch

import numpy as np

class Board:
    def __init__(self):
        self.data = np.zeros((3,3))

print("Tic Tac Toe ver 0")
board = Board()
print(board.data)