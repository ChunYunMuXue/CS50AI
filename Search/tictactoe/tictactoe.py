"""
Tic Tac Toe Player
"""

import math
import copy

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
    c1 = int(0)
    c2 = int(0)
    for L in board:
        for R in L:
            if R == X:c1 += 1
            if R == O:c2 += 1
    # print(c1,c2)
    if(c1 ^ c2 == 0):return X
    else:return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    ans = set()
    for x in range(0,3):
        for y in range(0,3):
            # print(board[x][y],end=' ')
            if(board[x][y] == EMPTY):ans.add((x,y))
        # print("")
    return ans
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x,y = action[0],action[1]
    C = player(board)
    ans = copy.deepcopy(board)
    if(ans[x][y] != EMPTY):raise ValueError
    ans[x][y] = C
    return ans
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if(board[0][0] == board[0][1] and board[0][1] == board[0][2] and (not board[0][0] == EMPTY)):return board[0][0]
    if(board[0][0] == board[1][0] and board[1][0] == board[2][0] and (not board[0][0] == EMPTY)):return board[0][0]
    if(board[0][0] == board[1][1] and board[1][1] == board[2][2] and (not board[0][0] == EMPTY)):return board[0][0]
    if(board[0][1] == board[1][1] and board[1][1] == board[2][1] and (not board[0][1] == EMPTY)):return board[0][1]
    if(board[0][2] == board[1][2] and board[1][2] == board[2][2] and (not board[0][2] == EMPTY)):return board[0][2]
    if(board[0][2] == board[1][1] and board[1][1] == board[2][0] and (not board[0][2] == EMPTY)):return board[0][2]
    if(board[1][0] == board[1][1] and board[1][1] == board[1][2] and (not board[1][0] == EMPTY)):return board[1][0]
    if(board[2][0] == board[2][1] and board[2][1] == board[2][2] and (not board[2][0] == EMPTY)):return board[2][0]
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    p = bool(1);
    for i in range(0,3):
        for j in range(0,3):
            p = p and (not board[i][j] == EMPTY)
    if p : return True
    if(not (winner(board) == None)):return True
    else:return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) == X):return 1
    if(winner(board) == O):return -1
    return 0
    raise NotImplementedError

val = {}

def findkey(board):
    key = ""
    for x in range(0,3):
        for y in range(0,3):
           if(board[x][y] == X):key += "X"
           if(board[x][y] == O):key += "O"
           if(board[x][y] == EMPTY):key += "E" 
    return key    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # print("START")
    # print(board)
    if(terminal(board)):
        val[findkey(board)] = utility(board)
        return None
    # print("AND")
    now = player(board)
    ans = (-1,-1)
    k = int(0)
    # for max
    S = actions(board)
    if now == X:
        k = int(-2)
        for s in S:
            # if(not findkey(result(board,s)) in val):raise ValueError
            # print("CHANGE ",s)
            si = minimax(result(board,s))
            # si = result(board,s)
            # print("RETURN ",board)
            ST = findkey(result(board,s))
            if(val[ST] > k):
                k = val[ST]
                ans = s
                if(k == 1):break
    if now == O:
        k = int(2)
        for s in S:
            # print("CHANGE ",s)
            si = minimax(result(board,s))
            ST = findkey(result(board,s))
            if(val[ST] < k):   
                k = val[ST]
                ans = s
                if(k == -1):break
    val[findkey(board)] = k
    # print(board)
    # print("END")
    return ans
    raise NotImplementedError

# SS = result([[X, EMPTY, EMPTY],
#             [EMPTY, X, EMPTY],
#             [EMPTY, EMPTY, X]],(0,1))

# print(terminal([[O, X, EMPTY],
#             [EMPTY, X, O],
#             [EMPTY, X, EMPTY]]))

# print(result([[X, EMPTY, EMPTY],
#             [EMPTY, EMPTY, EMPTY],
#             [EMPTY, EMPTY, EMPTY]],(0,1)))

# print(SS = actions([['O', 'X', None], [None, None, 'O'], [None, 'X', None]]))
# result([['O', 'X', None], [None, None, 'O'], [None, 'X', None]],)