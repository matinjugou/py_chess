from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class p_chessboard(QGraphicsPixmapItem):
    pic = QPixmap()

    placeChess = pyqtSignal(QPointF, name='')

    def __init__(self, parent: QGraphicsPixmapItem = None):
        super(p_chessboard, self).__init__()
        pass

    def __init__(self, str, parent: QGraphicsPixmapItem = None):
        super(p_chessboard, self).__init__()
        pic = QPixmap(str)
        self.se
        pass

    def mousePressEvent(self, event):
        self.placeChess.emit(event.pos())
        pass
