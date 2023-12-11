"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    n_x = 0
    n_o = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == X:
                n_x += 1
            elif board[i][j] == O:
                n_o += 1
    if n_x > n_o:
        return O
    return X

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_save = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if board[i][j] == EMPTY and 0 <= i < 3 and 0 <= j < 3:
        board_save[i][j] = player(board)
    else:
        raise ValueError
    return board_save

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0, 3):
        if board[i] == [X, X, X]:
            return X
        elif board[i] == [O, O, O]:
            return O

    for j in range(0, 3):
        col = []
        for i in range(0, 3):
            col.append(board[i][j])
        if col == [X, X, X]:
            return X
        elif col == [O, O, O]:
            return O
    diag1 = []
    diag2 = []
    for i in range(0, 3):
        diag1.append(board[i][i])
        diag2.append(board[i][3-i-1])
    if diag1 == [X, X, X] or diag2 == [X, X, X]:
        return X
    elif diag1 == [O, O, O] or diag2 == [O, O, O]:
        return O
    return None

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    n = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] != EMPTY:
                n += 1
    if n < 9:
        return False
    return True

    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0

    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    res = None
    if is_empty(board):
        res = (1, 1)
        return res
    if player(board) == X:
        v = -math.inf
        res = None
        for action in actions(board):
            value = min_value(result(board, action))
            if value > v:
                v = value
                res = action
    elif player(board) == O:
        v = math.inf
        res = None
        for action in actions(board):
            value = max_value(result(board, action))
            if value < v:
                v = value
                res = action
    return res

    # raise NotImplementedError


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def is_empty(board):
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] != EMPTY:
                return False
    return True
