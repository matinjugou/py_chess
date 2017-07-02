from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from abc import ABCMeta, abstractclassmethod


class PItem(QGraphicsPixmapItem):
    __metaclass__ = ABCMeta

    def __init__(self, parent:QGraphicsPixmapItem = None):
        QGraphicsPixmapItem.__init__(self, parent)
        pass

    def __init__(self, pic:QPixmap, parent:QGraphicsPixmapItem = None):
        QGraphicsPixmapItem.__init__(self,pic)
        pass