#################################################
# hw7.py
#
# Your Name:
# Your Andrew ID:
# Collaborators:
# (collaborators = comma separated andrew ids)
#################################################

from cmu_112_graphics import App
import copy

####################################
# Add your hw4, hw5 and hw6 functions here!
# You may need to modify them a bit.
####################################

def areLegalValues(values):
    for i in values:
        if (i != 0 and values.count(i) > 1) or i > len(values):
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


####################################
# SudokuApp
####################################

class PlaySudoku(App):
    def appStarted(self, board):
        self.game = SudokuGame(board)
        self.board = copy.deepcopy(board)
        self.ogBoard = copy.deepcopy(board)
        self.margin = 30
        self.cellWidth = (self.width-2*self.margin)//len(board[0])
        self.cellHeight = (self.height-2*self.margin)//len(board)
        self.hrow = 0
        self.hcol = 0
        self.gameOver = False
        self.time = 0
        self.rows = len(board)
        self.cols = len(board[0])
        self.moves = []
        self.undoMoves = []
        self.count = 0
        # TODO: more data initialization

    def getState(self):
        return (self.board, self.time)

    def checkGameOver(self):
        for i in range(self.rows):
            if 0 in self.board[i]:
                return self.gameOver
        self.gameOver = True
        return self.gameOver

    def keyPressed(self, event):
        # use event.key
        # you may find this helpful:
        # if event.key.isdigit():
        #     print(event.key)
        if not self.gameOver:
            if event.key == "Down":
                self.hrow = (self.hrow + 1) % len(self.board)
            elif event.key == "Up":
                self.hrow = (self.hrow - 1) % len(self.board)
            elif event.key == "Left":
                self.hcol = (self.hcol - 1) % len(self.board)
            elif event.key == "Right":
                self.hcol = (self.hcol + 1) % len(self.board)
            elif event.key.isdigit() and event.key != "0" and self.ogBoard[self.hrow][self.hcol] == 0:
                self.board[self.hrow][self.hcol] = int(event.key)
                if isLegalSudoku(self.board) == False:
                    self.board[self.hrow][self.hcol] = 0
                else:
                    self.moves += [(self.hrow, self.hcol, 0, int(event.key))]
                    self.undoMoves = []
                    self.checkGameOver() 
            elif event.key == "0" and self.ogBoard[self.hrow][self.hcol] == 0:
                oldNum = self.board[self.hrow][self.hcol]
                self.board[self.hrow][self.hcol] = 0
                self.moves += [(self.hrow, self.hcol, oldNum, 0)]
                self.undoMoves = []
            elif event.key == "u":
                self.undoMove()
            elif event.key == "r":
                self.redoMove()
        else:
            if event.key == "r":
                self.appStarted(self.ogBoard)  

    def mousePressed(self, event):
        # use event.x and event.y
        if (event.x >= self.margin and event.x < self.width - 2*self.margin and
            event.y >= self.margin and event.y < self.width - 2*self.margin):
            self.hrow = (event.y - self.margin) // self.cellHeight
            self.hcol = (event.x - self.margin) // self.cellWidth

    def timerFired(self):
        self.count += 1
        if self.count % 10 == 0:
            self.time += 1

    def redrawAll(self, canvas):
        # TODO: draw board
        self.drawSudokuBoard(canvas)
        canvas.create_text(self.width//2, self.margin//2, text = self.time, font = "Arial 15 bold")
        if self.gameOver:
            canvas.create_text(self.width // 2, self.height // 2, text = "Congratulations, You Won!", 
                               font = "Arial 26 bold", fill = "purple" )
        # TODO: draw other parts of your animation too!
    
    def drawSudokuBoard(self, canvas):
        canvas.create_rectangle(self.margin, self.margin, 
                                self.cols*self.cellWidth + self.margin, self.rows*self.cellHeight + self.margin, width=5)
        blockSize = self.cols**0.5
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j*self.cellWidth + self.margin, i*self.cellHeight + self.margin
                x2, y2 = x1+self.cellWidth, y1+self.cellHeight

                if i == self.hrow and j == self.hcol:
                    canvas.create_rectangle(x1, y1, x2, y2, fill = "yellow", tag = f"board[{i}][{j}]")
                else:
                    canvas.create_rectangle(x1,y1,x2,y2, tag = f"board[{i}][{j}]")
                
                if self.board[i][j] != 0:
                    if self.board[i][j] == self.ogBoard[i][j]:
                        canvas.create_text(x1+self.cellWidth//2, y1+self.cellHeight//2, text=self.board[i][j])
                    else:
                        canvas.create_text(x1+self.cellWidth//2, y1+self.cellHeight//2, text=self.board[i][j], fill = "red")

                if i%blockSize == 0:
                    canvas.create_line(self.margin, self.margin + i * self.cellHeight,
                                    self.cols*self.cellWidth + self.margin, self.margin + i * self.cellHeight,
                                    width = 5)

                if j % blockSize == 0:
                    canvas.create_line(self.margin + j * self.cellWidth, self.margin,
                                    self.margin + j * self.cellWidth, self.height - self.margin, 
                                    width = 5)

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

####################################
# Animation Tests!
####################################

def smallSudokuBoard():
    return [
        [1, 2, 3, 4],
        [4, 3, 0, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]
    ]


def bigSudokuBoard():
    return [
        [ 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
        [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
        [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
        [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
        [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
        [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
        [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
        [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
    ]


def testSudokuKeyPressed():
    print("testing sudoku keypressed", end="...")
    initialBoard = smallSudokuBoard()
    app = PlaySudoku(copy.deepcopy(initialBoard), isTest=True) # note this
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 0, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])
    # first highlighted cell is (0, 0)
    # we can move using Up/Down/Left/Right
    app.simulateKeyPress("Up")
    app.simulateKeyPress("Down")
    app.simulateKeyPress("Left")
    app.simulateKeyPress("Right")
    # this is with wraparound, so we should be back at 0, 0

    # we can wraparound as many times as we want
    for i in range(len(board)**2):
        app.simulateKeyPress("Down")

    app.simulateKeyPress("Right")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Down")
    # we should be on (1, 2) now, which is empty

    # illegal numbers: board shouldn't change
    app.simulateKeyPress("9")
    board, time = app.getState()
    assert(board == initialBoard)

    # another illegal number: no change
    app.simulateKeyPress("3")
    board, time = app.getState()
    assert(board == initialBoard)

    # this one is legal: board should change
    app.simulateKeyPress("2")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])

    # we can press u to undo and r to redo
    app.simulateKeyPress("u")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 0, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])
    app.simulateKeyPress("r")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])

    # 0 or backspace clear the cell
    app.simulateKeyPress("0")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 0, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])
    # put it back
    app.simulateKeyPress("2")

    # let's win the game
    app.simulateKeyPress("Down")
    app.simulateKeyPress("1")
    app.simulateKeyPress("Left")
    app.simulateKeyPress("4")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 4, 1, 3],
        [3, 1, 4, 2]])

    # we can press 'r' to reset!
    app.simulateKeyPress("r")
    board, time = app.getState()
    assert(board == initialBoard)

    # for sanity, make sure we're in the right location
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Right")
    app.simulateKeyPress("Down")
    app.simulateKeyPress("2")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])

    print("passed!")


def testSudokuMousePressed():
    print("testing sudoku mousepressed", end="...")
    # since we already tested all the behavior in keypressed,
    # this is a shorter test!
    initialBoard = smallSudokuBoard()
    app = PlaySudoku(copy.deepcopy(initialBoard), isTest=True) # note this
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 0, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])

    # click on an open cell
    x, y = app.getCenterOfElementWithTag("board[1][2]")
    app.simulateMousePress(x, y)
    app.simulateKeyPress("2")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 0, 3],
        [3, 1, 4, 2]])

    # click the cell below it, then click in the margin (outside the board)
    # but we should still be have the same selected cell
    x, y = app.getCenterOfElementWithTag("board[2][2]")
    app.simulateMousePress(x, y)
    app.simulateMousePress(5, 2)
    app.simulateMousePress(app.width-5, app.height-3)
    app.simulateKeyPress("1")
    board, time = app.getState()
    assert(board == [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [2, 0, 1, 3],
        [3, 1, 4, 2]])
    print("passed!")

def testSudokuTimerFired():
    print("testing sudoku timerfired", end="...")
    initialBoard = smallSudokuBoard()
    app = PlaySudoku(copy.deepcopy(initialBoard), isTest=True) # note this
    board, time = app.getState()
    assert(time == 0)

    # do a bunch of actions that won't affect the timer
    for i in range(len(board)):
        app.simulateKeyPress("Down")
        app.simulateMousePress(0, 0)
        x, y = app.getCenterOfElementWithTag("board[0][0]")
        app.simulateMousePress(x, y)

    board, time = app.getState()
    assert(time == 0)

    # simulate time happening, which should affect the timer
    app.simulateTimerFire(1000)
    board, time = app.getState()
    assert(time == 1) # 1 second has elapsed

    app.simulateTimerFire(900)
    board, time = app.getState()
    assert(time == 1) # not quite another full second, so it should still be 1

    app.simulateTimerFire(100)
    board, time = app.getState()
    assert(time == 2) # now it is 2

    app.simulateTimerFire(500*1000) # 3 minutes
    board, time = app.getState()
    assert(time == 2 + 500)
    print("passed!")


def testPlaySudoku():
    print("testing PlaySudoku", end="...")
    testSudokuKeyPressed()
    # TODO: uncomment these when you're ready!
    testSudokuMousePressed()
    testSudokuTimerFired()
    print("passed!")


####################################
# Main
####################################


def main():
    testPlaySudoku()
    sudokuBoard = bigSudokuBoard()
    PlaySudoku(sudokuBoard, width=800, height=800)
    sudokuBoard = smallSudokuBoard()
    PlaySudoku(sudokuBoard, width=800, height=800)


if __name__ == "__main__":
    main()
