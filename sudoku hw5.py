import basic_graphics

def drawSudokuBoard(canvas, width, height, board, margin):
    canvas.create_rectangle(margin, margin, width-margin, height-margin, width=5)
    cellWidth = (width-2*margin)//len(board[0])
    cellHeight = (height-2*margin)//len(board)
    rows = len(board)
    cols = len(board[0])
    blockSize = cols**0.5
    for i in range(rows):
        for j in range(cols):    
            x1, y1 = j*cellWidth + margin, i*cellHeight + margin
            x2, y2 = x1+cellWidth, y1+cellHeight
            canvas.create_rectangle(x1,y1,x2,y2)
            canvas.create_text(x1+cellWidth//2, y1+cellHeight//2, text=board[i][j])

            if i%blockSize == 0:
                canvas.create_line(margin, margin + i * cellHeight,
                                   width - margin, margin + i * cellHeight,
                                   width = 5)
            
            if j % blockSize == 0:
                canvas.create_line(margin + j * cellWidth, margin,
                                   margin + j * cellWidth, height - margin, 
                                   width = 5)

def getSudokuBoard0():
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

def getSudokuBoard1():
    return [
        [1,2,3,4],
        [3,4,5,6],
        [7,8,9,10],
        [11,12,13,14]
    ]

def testDrawSudoku():
    print("Testing drawSudokuBoard()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    basic_graphics.run(getSudokuBoard0(), 10, drawFn=drawSudokuBoard)
    basic_graphics.run(getSudokuBoard1(), 10, drawFn=drawSudokuBoard)
    print("Done!")

testDrawSudoku()