import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PChessBoard(QGraphicsPixmapItem):

    placeChess = pyqtSignal(QPointF, name='placeChess')

    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()

        # chessboard visual
        ##self.setGeometry(100, 100, 800, 800)
        ##self.setScaledContents(True)
        self.pic_chessboard = QPixmap("resources//pic//chessboard.bmp")
        self.setPixmap(self.pic_chessboard)

        # some geometrical argument
        self.left_up_x = 30
        self.left_up_y = 30
        self.right_down_x = 770
        self.right_down_y = 770
        self.space = (self.right_down_x - self.left_up_x) / 14
        '''
        # some argument for a play
        self.num_pieces = 0;

        '''


# base class
class ChessMan(QGraphicsPixmapItem):
    def __init__(self, x = 0, y = 0, parent = None):
        super(ChessMan, self).__init__(parent)
        self.able_to_play = False
        self.index_pos = (x, y)
        pass

    def set_index_pos(self, x, y):
        self.index_pos = (x, y)


# black ChessMan class
class BlackChessMan(ChessMan):
    def __init__(self, x = 0, y = 0, parent = None):
        super(BlackChessMan, self).__init__(x, y, parent)
        self.pic_black_chess_man = QPixmap("resources//pic//blackpiece.bmp")
        self.setPixmap(self.pic_black_chess_man)
        self.index_pos = (x, y)
        pass


# white ChessMan class
class WhiteChessMan(ChessMan):
    def __init__(self, x = 0, y = 0, parent = None):
        super(WhiteChessMan, self).__init__(x, y, parent)
        self.pic_whiteChessMan = QPixmap("resources//pic//whitepiece.bmp")
        self.setPixmap(self.pic_whiteChessMan)
        self.index_pos = (x, y)
        pass