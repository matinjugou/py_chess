from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class PChessBoard(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()

        # chessboard visual
        self.pic_chessboard = QPixmap("resources//pic//chessboard.bmp")
        self.setPixmap(self.pic_chessboard)

        # some geometrical argument
        self.left_up_x = 20
        self.left_up_y = 20
        self.right_down_x = 513
        self.right_down_y = 513
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
        self.pic_black_chess_man = QPixmap("resources//pic//blackpiece.png")
        self.setPixmap(self.pic_black_chess_man)
        self.index_pos = (x, y)
        pass


# white ChessMan class
class WhiteChessMan(ChessMan):
    def __init__(self, x = 0, y = 0, parent = None):
        super(WhiteChessMan, self).__init__(x, y, parent)
        self.pic_whiteChessMan = QPixmap("resources//pic//whitepiece.png")
        self.setPixmap(self.pic_whiteChessMan)
        self.index_pos = (x, y)
        pass


# background of the start menu
class PStartMenuBackGround(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()

        # menu visual
        self.pic_startMenu = QPixmap("resources//pic//startMenu.jpg")
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

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
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

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_machine_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_machine_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


class PStartMenu_Online(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        # online label
        self.pic_online_1 = QPixmap("resources//pic//online_1.png")
        self.pic_online_2 = QPixmap("resources//pic//online_2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_online_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_online_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_online_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


class PStartMenu_Net(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()

        # multiple label
        self.pic_net_1 = QPixmap("resources//pic//multiple1.png")
        self.pic_net_2 = QPixmap("resources//pic//multiple2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_net_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_net_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_net_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


class PReturn(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super(PReturn, self).__init__()
        # machine label

        self.pic_return_1 = QPixmap("resources//pic//return1.png")
        self.pic_return_2 = QPixmap("resources//pic//return2.png")
        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_return_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_return_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_return_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


# cursor
class PSquare(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        self.pic_square_white = QPixmap("resources//pic//square_white.png")
        self.pic_square_black = QPixmap("resources//pic//square_black.png")
        self.setPixmap(self.pic_square_black)


class PWaitingBoard(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        self.background = QPixmap("resources//pic//waitBoard.jpg")
        self.setPixmap(self.background)


# another background image
class PPicture_Supplement(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        self.pic_supplement = QPixmap("resources//pic//wood.jpg")
        self.setPixmap(self.pic_supplement)


# undo
class PUndo(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        self.pic_undo_1 = QPixmap("resources//pic//regret_1.png")
        self.pic_undo_2 = QPixmap("resources//pic//regret_2.png")

        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_undo_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_undo_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_undo_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)


# Save
class PSave(QGraphicsPixmapItem):
    def __init__(self, parent: QGraphicsPixmapItem = None):
        super().__init__()
        self.pic_save_1 = QPixmap("resources//pic//save_1.png")
        self.pic_save_2 = QPixmap("resources//pic//save_2.png")

        self.setAcceptHoverEvents(True)
        self.setPixmap(self.pic_save_1)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_save_2)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setPixmap(self.pic_save_1)
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)