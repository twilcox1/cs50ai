"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    flat = [single_square for row_list in board for single_square in row_list]
    x = flat.count('X')
    o = flat.count('O')
    if x > o:
        return O
    elif x <= o:
        return X


def actions(board):
    possible_moves = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is not None:
                possible_moves.add((i, j))
    return possible_moves



def result(board, action):
    current = player(board)
    deep_board = copy.deepcopy(board)
    row, cell = action
    deep_board[row][cell] = current




def winner(board):
    row = check_row(board)
    if row is not None:
        return row
    column = check_column(board)
    if column is not None:
        return column
    left_diag = check_left_diag(board)
    if left_diag is not None:
        return left_diag
    right_diag = check_right_diag(board)
    if right_diag is not None:
        return right_diag
    return None


def terminal(board):
    won = winner(board)
    if won is not None:
        return True
    return check_draw(board)


def utility(board):
    won = winner(board)
    if won is not None:
        return 1 if won == X else -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

def check_column(board):
    size = len(board)
    for num in range(size):
        column = [board[row][num] for row in range(size)]
        if len(set(column)) == 1 and column[0] is not None:
            return column[0]

def check_row(board):
    for row in board:
        if row[0] is not None:
            if len(set(row)) == 1:
                return row[0]
            else:
                return None
            
def check_left_diag(board):
    size = len(board)
    diag = []
    for num in range(size):
        diag.append(board[num][num])
    if len(set(diag)) == 1 and diag[0] is not None:
        return diag[0]
    else:
        return None

def check_right_diag(board):
    size = len(board)
    diag = [board[num][size - 1 - num] for num in range(size)]
    if len(set(diag)) == 1 and diag[0] is not None:
        return diag[0]
    else:
        return None
    
def check_draw(board):
    flat = {cell for row in board for cell in row}
    return None not in flat



