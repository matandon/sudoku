#################################################
# hw6.py
#
# Your name:
# Your andrew id:
# Collaborators:
# (collaborators = comma separated andrew ids)
#################################################

import copy
import decimal

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

######################################################################
# Your Functions and OOP class definitions
######################################################################

def areLegalValues(values):
    for i in range(0, len(values)):
        if values[i] != 0 and values.count(values[i]) > 1:
            return False
    return True


def isLegalRow(board, row):
    L = board[row]
    if not areLegalValues(L):
        return False
    return True


def isLegalCol(board, col):
    a = []
    for row in range(len(board)):
        a += [board[row][col]]
    if not areLegalValues(a):
        return False
    return True

def isLegalBlock(board, block):
    N = int(len(board)**0.5)
    blockL = []
    for row in range(N):
        for col in range(N):
            blockL += [board[row + N*(block//N)][(col + (block%N)*N)]]
    if not areLegalValues(blockL):
        return False
    return True

def isLegalSudoku(board):
    for row in range(len(board)):
        if isLegalRow(board, row) == False:
            return False
    for col in range(len(board[0])):
        if isLegalCol(board, col) == False:
            return False
    for block in range(len(board)):
        if isLegalBlock(board, block) == False:
            return False
    return True

class SudokuGame(object):
    def __init__(self, board):
        self.originalBoard = copy.deepcopy(board)
        self.board = copy.deepcopy(board)
        self.rows = len(board)
        self.cols = len(board[0])
        self.N = len(board)**0.5
        self.moves = []
        self.undoMoves = []
        self.gameOver = False

    def getBoard(self):
        return self.board
    
    def placeNumber(self, row, col, num):
        oldNum = self.board[row][col]
        self.moves += [(row, col, self.board[row][col], num)]
        self.board[row][col] = num
        if not isLegalSudoku(self.board) or self.originalBoard[row][col] != 0:
            self.board[row][col] = oldNum
            self.moves.pop()
            return False
        self.undoMoves = []
        return True
    
    def undoMove(self):
        if self.moves != []:
            row, col, ogNum, numInSpot = self.moves.pop()
            self.board[row][col] = ogNum
            self.undoMoves += [(row, col, numInSpot, ogNum)]
            return True
        return False
    
    def redoMove(self):
        if self.undoMoves != []:
            row, col, oldNum, newNum = self.undoMoves[0] 
            self.board[row][col] = oldNum
            self.moves += [(row, col, newNum, oldNum)]
            return True
        return False 

    def checkGameOver(self):
        for i in range(self.rows):
            if 0 in self.board[i]:
                return self.gameOver
        self.gameOver = True
        return self.gameOver

#################################################################
# Test Functions
#################################################################


def testSudokuGame():
    print("testing SudokuGame...")
    game = SudokuGame([
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ])
    # game isn't over at the beginning!
    assert(game.checkGameOver() == False)
    # can't override original squares!
    assert(game.placeNumber(0, 0, 3) == False)
    assert(game.getBoard() == [
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ])
    assert(game.placeNumber(1, 1, 3))
    assert(game.placeNumber(0, 2, 3))
    assert(game.getBoard() == [
        [1, 2, 3, 4],
        [4, 3, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ])

    # undo the last move, then redo it
    assert(game.undoMove() == True)
    assert(game.getBoard() == [
        [1, 2, 0, 4],
        [4, 3, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ])
    assert(game.redoMove() == True)
    assert(game.getBoard() == [
        [1, 2, 3, 4],
        [4, 3, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ])

    # undo a move, then replace it with a new move
    assert(game.undoMove() == True)
    assert(game.undoMove() == True)
    assert(game.placeNumber(3, 0, 3))
    assert(game.getBoard() == [
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [3, 1, 4, 0]
    ])
    # this should do nothing, since we replaced the move
    assert(game.redoMove() == False)
    assert(game.getBoard() == [
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [3, 1, 4, 0]
    ])

    newGame = SudokuGame([
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 1, 3],
        [3, 1, 4, 2]
    ])
    assert(newGame.undoMove() == False)
    assert(newGame.getBoard() == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 1, 3],
        [3, 1, 4, 2]
    ])
    assert(newGame.checkGameOver() == False)
    assert(newGame.placeNumber(2, 1, 4))
    assert(newGame.checkGameOver() == True)
    print("passed!")


#################################################
# testAll and main
#################################################

def testAll():
    testSudokuGame()

def main():
    testAll()

if __name__ == "__main__":
    main()


