import copy

#################################################
# Sudoku Functions
#################################################

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

#################################################
# Test Functions
#################################################

def isNondestructive(f, L):  # Checks to make sure f(L) does not modify L
    unmodifiedCopy = copy.deepcopy(L)
    b = f(L)
    return L == unmodifiedCopy

def testAreLegalValues():
    print("Testing areLegalValues...", end="")
    assert(areLegalValues([1]) == True) # TODO
    assert(areLegalValues([0, 1]) == True) # TODO
    assert(areLegalValues([0, 1, 2, 3]) == True) # TODO
    assert(isNondestructive(areLegalValues, [0, 1, 2, 3]))
    print("Passed!")


def testIsLegalRow():
    print("Testing IsLegalRow...", end="")
    board0 = [
        [0, 2, 3, 4],
        [3, 0, 3, 1],
        [2, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    assert(isLegalRow(board0, 0) == True) # TODO
    assert(isLegalRow(board0, 1) == False) # TODO
    print("Passed!")


def testIsLegalCol():
    print("Testing IsLegalCol...", end="")
    board0 = [
        [0, 2, 3, 4],
        [3, 0, 3, 1],
        [2, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    assert(isLegalCol(board0, 0) == True) # TODO
    assert(isLegalCol(board0, 2) == False) # TODO
    print("Passed!")


def testIsLegalBlock():
    print("Testing IsLegalBlock...", end="")
    board1 = [
        [0, 2, 3, 4],
        [3, 0, 3, 1],
        [2, 1, 0, 4],
        [0, 0, 4, 0]
    ]
    assert(isLegalBlock(board1, 0) == True) # TODO
    assert(isLegalBlock(board1, 1) == False) # TODO
    assert(isLegalBlock(board1, 3) == False) # TODO
    print("Passed!")


def testIsLegalSudoku():
    testAreLegalValues()
    testIsLegalRow()
    testIsLegalCol()
    testIsLegalBlock()
    print("Testing isLegalSudoku...", end = "")
    board2 = [
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ]
    assert(isLegalSudoku(board2) == True) # TODO
    board3 = [
        [1, 2, 1, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ]
    assert(isLegalSudoku(board3) == False) # TODO
    board4 = [
        [1, 2, 0, 4],
        [4, 0, 2, 3],
        [2, 0, 0, 3],
        [0, 1, 4, 0]
    ]
    assert(isLegalSudoku(board4) == False) # TODO
    board5 = [
        [1, 2, 0, 4],
        [4, 0, 2, 0],
        [2, 0, 0, 3],
        [0, 1, 3, 0]
    ]
    assert(isLegalSudoku(board5) == False) # TODO
    bigBoard = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    assert(isLegalSudoku(bigBoard) == True)
    print("Passed!")


#################################################
# testAll and main
#################################################


def testAll():
    testIsLegalSudoku()


def main():
    testAll()


if __name__ == '__main__':
    main()
