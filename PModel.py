from PChessBoard import *
from collections import deque


PLAYER_WIN_PROFIT = 100
AI_WIN_PROFIT = -100
TIE_PROFIT = 0


class PModel(QGraphicsScene):
    def __init__(self, parent = None):
        super(PModel, self).__init__(parent)
    pass

'''
class PStartMenu(PModel):
    def __init__(self, parent = None):
        super(PStartMenu, self).__init__(parent)
        ##TODO:create a startmenu including single player and multiple player
    pass
'''

class PMultipleModel(PModel):
    def __init__(self, parent = None):
        super(PMultipleModel, self).__init__(parent)
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]

        # stack for black piece and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        '''
        TODO:trans it into current framework
        self.black_chess_cursor = QCursor(QPixmap("blackpiece.bmp"))
        self.white_chess_cursor = QCursor(QPixmap("whitepiece.bmp"))
        self.setCursor(self.black_chess_cursor)
        '''

        self.addItem(self.chessboard)
        pass

    # restart
    def restart(self):
        self.black_chessman_queue.clear()
        self.white_chessman_queue.clear()
        self.num_pieces = 0
        self.clear()
        self.chessboard = PChessBoard()
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        self.addItem(self.chessboard)

    # mouse press event
    def mousePressEvent(self, event):
        super(PMultipleModel, self).mousePressEvent(event)
        print(event.pos())
        if event.button() == Qt.LeftButton:
            print(event.pos().x(), event.pos().y())
            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.pos().x() <= self.chessboard.right_down_x + 20 and self.chessboard.left_up_y - 20 <= event.pos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.pos().x() - self.chessboard.left_up_x + 0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.pos().y() - self.chessboard.left_up_y + 0.25 * self.chessboard.space) / self.chessboard.space)
                # that space has not been set piece
                if self.situation_matrix[temp_row][temp_col] == 0:
                    # black chessman turn
                    if self.num_pieces % 2 == 0:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 1
                        temp_black_chessman = BlackChessMan(self)
                        temp_black_chessman.set_index_pos(temp_col, temp_row)
                        temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)

                        print("black_chess_index_pos (%d, %d)" %(temp_col, temp_row))
                        self.addItem(temp_black_chessman)
                        self.black_chessman_queue.append(temp_black_chessman)
                        # check for win
                        result = check_win_black(self.situation_matrix)
                        # if black wins
                        if result == 1:
                            print("black wins")
                            self.restart()
                        '''
                        else:
                            # change the cursor
                            self.setCursor(self.white_chess_cursor)
                        '''

                    else:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 2
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(temp_col, temp_row)
                        temp_white_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" %(temp_col, temp_row))
                        self.addItem(temp_white_chessman)
                        self.white_chessman_queue.append(temp_white_chessman)
                        # check for win
                        result = check_win_white(self.situation_matrix)
                        # if white wins
                        if result == 2:
                            print("white wins")
                            self.restart()
                        '''
                        else:
                            self.setCursor(self.black_chess_cursor)
                        '''
            pass


class PSingleModel(PModel):

    def __init__(self, parent:PModel = None):
        super(PSingleModel, self).__init__()
        self.scene = QGraphicsScene()
        self.chessboard = PChessBoard()

        self.chessboard.setPos(0, 0)
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]

        # stack for black piece and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        self.addItem(self.chessboard)
        pass

class Node:
    def __init__(self):
        self.choice = (0, 0)
        self.

    pass


# check win for black piece
# return value: 0 for not win, 2 for win
def check_win_black(matrix):
    # check for horizontal
    for i in range(0,15):
        for j in range(0,11):
            result = matrix[i][j] * matrix[i][j+1] * matrix[i][j+2] * matrix[i][j+3] * matrix[i][j+4]
            # check for 6 in a row
            if result == 1:
                if j - 1 >= 0 and j + 5 <= 14:
                    if matrix[i][j-1] != 1 and matrix[i][j+5] != 1:
                        return 1
                elif j - 1 < 0:
                    if matrix[i][j+5] != 1:
                        return 1
                elif j + 5 > 14:
                    if matrix[i][j-1] != 1:
                        return 1
                else:
                    a = 1

    # check for vertical
    for i in range(0,11):
        for j in range(0,15):
            result = matrix[i][j] * matrix[i+1][j] * matrix[i+2][j] * matrix[i+3][j] * matrix[i+4][j]
            # check for 6 in a row
            if result == 1:
                if i - 1 >= 0 and i + 5 <= 14:
                    if matrix[i-1][j] != 1 and matrix[i + 5][j] != 1:
                        return 1
                elif i - 1 < 0 :
                    if matrix[i + 5][j] != 1:
                        return 1
                elif i + 5 > 14:
                    if matrix[i-1][j] != 1:
                        return 1
                else:
                    a = 1

    # check for left-up
    for i in range(0,11):
        for j in range(0,11):
            result = matrix[i][j] * matrix[i+1][j+1] * matrix[i+2][j+2] * matrix[i+3][j+3] * matrix[i+4][j+4]
            if result == 1:
                if i == 0 or j == 0:
                    if  i != 10 or i != 10:
                        if matrix[i+5][j+5] != 1:
                            return 1
                    else:
                        return 1
                elif j == 10 or j == 10:
                    if matrix[i - 1][j - 1] != 1:
                        return 1
                else:
                    if matrix[i-1][j-1] != 1 and matrix[i+5][j+5] != 1:
                        return 1

    # check for right-up
    for i in range(0,11):
        for j in range(4,15):
            result = matrix[i][j] * matrix[i+1][j-1] * matrix[i+2][j-2] * matrix[i+3][j-3] * matrix[i+4][j-4]
            if result == 1:
                if i == 0 or j == 14:
                    if j != 4 or i != 10:
                        if matrix[i+5][j-5] != 1:
                            return 1
                    else:
                        return 1
                elif i == 10 or j == 4:
                    if matrix[i-1][j+1] != 1:
                        return 1
                else:
                    if  matrix[i-1][j+1] != 1 and matrix[i+5][j-5] != 1:
                        return 1

    return 0


# check win for white piece
# return value: 0 for not win, 2 for win
def check_win_white(matrix):
    # check for horizontal
    for i in range(0,15):
        for j in range(0,11):
            result = matrix[i][j] * matrix[i][j+1] * matrix[i][j+2] * matrix[i][j+3] * matrix[i][j+4]
            # check for 6 in a row
            if result == 32:
                if j - 1 >= 0 and j + 5 <= 14:
                    if matrix[i][j-1] != 2 and matrix[i][j+5] != 2:
                        return 2
                elif j - 1 < 0:
                    if matrix[i][j+5] != 2:
                        return 2
                elif j + 5 > 14:
                    if matrix[i][j-1] != 2:
                        return 2
                else:
                    a = 1

    # check for vertical
    for i in range(0,11):
        for j in range(0,15):
            result = matrix[i][j] * matrix[i+1][j] * matrix[i+2][j] * matrix[i+3][j] * matrix[i+4][j]
            # check for 6 in a row
            if result == 32:
                if i - 1 >= 0 and i + 5 <= 14:
                    if matrix[i-1][j] != 2 and matrix[i + 5][j] != 2:
                        return 2
                elif i - 1 < 0 :
                    if matrix[i + 5][j] != 2:
                        return 2
                elif i + 5 > 14:
                    if matrix[i-1][j] != 2:
                        return 2
                else:
                    a = 1

    # check for left-up
    for i in range(0,11):
        for j in range(0,11):
            result = matrix[i][j] * matrix[i+1][j+1] * matrix[i+2][j+2] * matrix[i+3][j+3] * matrix[i+4][j+4]
            if result == 32:
                if i == 0 or j == 0:
                    if  i != 10 or i != 10:
                        if matrix[i+5][j+5] != 2:
                            return 2
                    else:
                        return 2
                elif j == 10 or j == 10:
                    if matrix[i - 1][j - 1] != 2:
                        return 2
                else:
                    if matrix[i-1][j-1] != 2 and matrix[i+5][j+5] != 2:
                        return 2
    # check for right-up
    for i in range(0,11):
        for j in range(4,15):
            result = matrix[i][j] * matrix[i+1][j-1] * matrix[i+2][j-2] * matrix[i+3][j-3] * matrix[i+4][j-4]
            if result == 32:
                if i == 0 or j == 14:
                    if j != 4 or i != 10:
                        if matrix[i+5][j-5] != 2:
                            return 2
                    else:
                        return 2
                elif i == 10 or j == 4:
                    if matrix[i-1][j+1] != 2:
                        return 2
                else:
                    if  matrix[i-1][j+1] != 2 and matrix[i+5][j-5] != 2:
                        return 2

    return 0
