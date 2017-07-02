from PyQt5.QtWidgets import (QGraphicsObject, QGraphicsView, QGraphicsScene, QApplication)
from PyQt5.Qt import QObject
from p_chess_board import p_chessboard
from PyQt5.QtCore import *

class p_multiple_model(QObject):

    def __init__(self,parent:QObject = None):
        super(p_multiple_model, self).__init__()
        self.scene = QGraphicsScene()
        self.chessboard = p_chessboard()

        self.scene.addItem(self.chessboard)

        self.chessboard.placeChess.connect(self.place_chess())
        pass

    def place_chess(self, pos:QPointF):

        pass