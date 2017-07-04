import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# background of the start menu
class PStartMenuBackGround(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()

        # menu visual
        self.pic_startMenu =  QPixmap("resources//pic//startMenu.jpg")
        self.setPixmap(self.pic_startMenu)

# visual label of multiple model
class PStartMenu_Multiple(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()


        # multiple label
        self.pic_multiple_1 = QPixmap("resources//pic//multiple1.png")
        self.pic_multiple_2 = QPixmap("resources//pic//multiple2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_multiple_1)

        
    def hoverEnterEvent(self,QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_multiple_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)
    
    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_multiple_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


class PStartMenu_Machine(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        # machine label
        self.pic_machine_1 = QPixmap("resources//pic//machine1.png")
        self.pic_machine_2 = QPixmap("resources//pic//machine2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_machine_1)

    def hoverEnterEvent(self,QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_machine_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)
    
    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_machine_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


class PReturn(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        # machine label

        self.pic_return_1 =  QPixmap("resources//pic//return1.png")
        self.pic_return_2 =  QPixmap("resources//pic//return2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_return_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_return_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_return_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

        


