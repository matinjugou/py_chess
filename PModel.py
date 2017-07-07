from PChessBoard import *
from collections import deque
from PStartMenuView import *
from SaveAndLoad import *
import numpy as np
import copy as copy
import socket
import time
import threading


class PModel(QGraphicsScene):
    def __init__(self, parent: 'QGraphicsScene' = None):
        super(PModel, self).__init__(parent)
    pass

# start menu
class PStartMenu(PModel):
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent: 'PModel' = None):
        super(PStartMenu, self).__init__(parent)
        self.startMenu = PStartMenuBackGround()
        self.startMenu.setPos(0, 0)


        # multiple label
        self.multipleLabel = PStartMenu_Multiple()
        self.multipleLabel.setPos(400, 10)

        # machine label
        self.machineLabel = PStartMenu_Machine()

        self.machineLabel.setPos(400, 80)

        # online label
        self.onlineLabel = PStartMenu_Online()
        self.onlineLabel.setPos(385,150)
        
        # add the item
        self.addItem(self.startMenu)
        self.addItem(self.machineLabel)
        self.addItem(self.multipleLabel)

        self.addItem(self.onlineLabel)
    pass

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print(event.scenePos().x(),event.scenePos().y())
        if 385.0 <= event.scenePos().x() <= 680.0:
            if 10.0 <= event.scenePos().y() <= 80.0:
                self.Signal_ChangeModel.emit(2)
            elif 80.0 <= event.scenePos().y() <= 150.0:
                self.Signal_ChangeModel.emit(3)
            elif 150.0 <= event.scenePos().y() <= 220.0:
                self.Signal_ChangeModel.emit(4)
            pass


class PMultipleModel(PModel):
     #signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent = None):
        super(PMultipleModel, self).__init__(parent)
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100,0)

        # stack for black piece and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        # cursor square
        self.square = PSquare()

        # Save label
        self.saveLabel = PSave()
        self.saveLabel.setPos(540,310)

        # undo label
        self.undoLabel = PUndo()
        self.undoLabel.setPos(540,380)

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540,450)

        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.square)
        self.addItem(self.saveLabel)
        self.addItem(self.returnLabel)
        self.addItem(self.undoLabel)
        pass

    # restart
    def restart(self):
        self.black_chessman_queue.clear()
        self.white_chessman_queue.clear()
        self.num_pieces = 0
        self.clear()
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]

        self.chessboard = PChessBoard()

        # supplement pic
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100,0)

        # cursor
        self.square = PSquare()
        self.square.hide()



        # undo label
        self.undoLabel = PUndo()
        self.undoLabel.setPos(540,380)

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540,450)

        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.square)
        self.addItem(self.saveLabel)
        self.addItem(self.returnLabel)
        self.addItem(self.undoLabel)

    # mouse move event
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super(PMultipleModel, self).mousePressEvent(event)
        # if on the chess board
        if self.chessboard.left_up_x - 20.0 <= event.scenePos().x() <= self.chessboard.right_down_x + 20.0 \
                and self.chessboard.left_up_y - 20.0 <= event.scenePos().y() <= self.chessboard.right_down_y + 20.0:
            temp_col = int((event.scenePos().x() - self.chessboard.left_up_x
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            temp_row = int((event.scenePos().y() - self.chessboard.left_up_y
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            # that space has not been set piece
            if self.situation_matrix[temp_row][temp_col] == 0:
                self.square.show()
                if self.num_pieces % 2 == 0:
                    self.square.setPixmap(self.square.pic_square_black)
                else:
                    self.square.setPixmap(self.square.pic_square_white)
                self.square.setPos(self.chessboard.space
                                   * (temp_col) - 17 + 20, self.chessboard.space * (temp_row) - 17 + 20)
            else:
                self.square.hide()

    # undo label
    def Undo(self):
        if self.num_pieces > 0:

            # if black just set a chessman
            if  self.num_pieces % 2 == 1:
                temp_row, temp_col = self.black_chessman_queue[-1].index_pos
                print('{},{}'.format(temp_row, temp_col))
                self.removeItem(self.black_chessman_queue.pop())
                self.situation_matrix[temp_row][temp_col] = 0
                self.num_pieces -= 1
            # if white just set a chessman
            else:
                temp_row , temp_col = self.white_chessman_queue[-1].index_pos
                print('{},{}'.format(temp_row, temp_col))
                self.removeItem(self.white_chessman_queue.pop())
                self.situation_matrix[temp_row][temp_col] = 0
                self.num_pieces -= 1

    # mouse press event
    def mousePressEvent(self, event):
        super(PMultipleModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton:
            print(event.scenePos().x(), event.scenePos().y())

            # if on the save button
            if 540 <= event.scenePos().x() <= 690 and 310 <= event.scenePos().y() <= 380:
                Save_ChessBoard(self.situation_matrix,"multiple.txt")

            # if on the undo button
            if 540 <= event.scenePos().x() <= 690 and 380 <= event.scenePos().y() <= 440:
                self.Undo()

            # if on the return button
            if 540 <= event.scenePos().x() <= 690 and 450 <= event.scenePos().y() <= 520:
                self.Signal_ChangeModel.emit(1)

            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20\
                    and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.scenePos().x() - self.chessboard.left_up_x +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.scenePos().y() - self.chessboard.left_up_y +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                # that space has not been set piece
                if self.situation_matrix[temp_row][temp_col] == 0:
                    # black chessman turn
                    if self.num_pieces % 2 == 0:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 1
                        temp_black_chessman = BlackChessMan(self)
                        temp_black_chessman.set_index_pos(temp_row, temp_col)
                        temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)

                        print("black_chess_index_pos (%d, %d)" %(temp_row, temp_col))
                        self.addItem(temp_black_chessman)
                        self.black_chessman_queue.append(temp_black_chessman)
                        # check for win
                        result = check_win_black(self.situation_matrix)
                        # if black wins
                        if result == 1:
                            print("black wins")
                            self.end_game(player = 1)

                    else:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 2
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(temp_row, temp_col)
                        temp_white_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" %(temp_row, temp_col))
                        self.addItem(temp_white_chessman)
                        self.white_chessman_queue.append(temp_white_chessman)
                        # check for win
                        result = check_win_white(self.situation_matrix)
                        # if white wins
                        if result == 2:
                            print("white wins")
                            self.end_game(player = 2)

            pass

    # win notification
    def end_game(self, player):
        # black wins
        if player == 1:
            button = QMessageBox.question(None,"胜利！",
                                    self.tr("黑方获胜！"),
                                    QMessageBox.Ok|QMessageBox.Cancel,
                                    QMessageBox.Ok)
        # white wins
        else:
            button = QMessageBox.question(None,"胜利！",
                                    self.tr("白方获胜！"),
                                    QMessageBox.Ok|QMessageBox.Cancel,
                                    QMessageBox.Ok)

        if button == QMessageBox.Ok:
            self.restart()
        else:
            self.restart()


class Board(object):
    # board for game

    def __init__(self):
        self.width = 15
        self.height = 15
        # represent the status of the chessboard,
        # 0 standing for nothing, 1 standing for black, 2 standing for white
        self.status = np.zeros(225)
        self.states = {}  # board states, key:(player, move), value: piece type
        self.n_in_row = 5  # need how many pieces in a row to win
        self.available = list(range(self.width * self.height)) # available moves
        for m in self.available:
            self.states[m] = -1
        pass

    def move_to_location(self, move):
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(225):
            return -1
        return move

    def update(self, player, move):
        self.states[move] = player
        self.available.remove(move)
        self.status[move] = (player + 1) % 2 + 1


# the model in which people play with AI.
# temporarily, we rule it that AI go first using white chessman
class PSingleModel(PModel):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, single_move_time=5, max_actions=1000, parent: PModel = None):
        super(PSingleModel, self).__init__()
        # some arguments for a play
        self.num_pieces = 0
        self.board = Board()
        self.n_in_row = 5
        # level of difficiculty(default = 1)
        self.level = 1
        # init UI
        # main scene
        self.scene = QGraphicsScene()
        # main chess board
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        #picture supplement
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100,0)
        # cursor square
        self.square = PSquare()
        # return label
        self.returnLabel = PReturn()

        self.returnLabel.setPos(540, 450)
        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)

        # chose the level
        customMsgBox = QMessageBox(None)
        customMsgBox.setWindowTitle("难度选择")
        easyButton = customMsgBox.addButton(self.tr("简单"),
                                            QMessageBox.ActionRole)
        hardButton = customMsgBox.addButton(self.tr("困难"),
                                              QMessageBox.ActionRole)

        customMsgBox.setText(self.tr("请选择难度：简单/困难"))
        customMsgBox.exec_()

        button = customMsgBox.clickedButton()
        if button == easyButton:
            self.level = 1
        elif button == hardButton:
            self.level = 2
        else:
            pass

    # strategy functions
    def get_move_easy(self):
        empty = 0
        black_num = 0
        white_num = 0
        value_list = np.zeros(225)
        for x in range(15):
            for y in range(15):
                if self.board.status[x * 15 + y] == 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                for k in range(1, 5):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.status[(x + k * i) * 15 + y + k * j] == 1:
                                            black_num += 1
                                        elif self.board.status[(x + k * i) * 15 + y + k * j] == 0:
                                            empty += 1
                                            break
                                        else:
                                            break
                                for k in range(-1, -5, -1):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.status[(x + k * i) * 15 + y + k * j] == 1:
                                            black_num += 1
                                        elif self.board.status[(x + k * i) * 15 + y + k * j] == 0:
                                            empty += 1
                                            break
                                        else:
                                            break
                                if black_num == 1:
                                    value_list[x * 15 + y] += 1
                                elif black_num == 2:
                                    if empty == 1:
                                        value_list[x * 15 + y] += 5
                                    elif empty == 2:
                                        value_list[x * 15 + y] += 10
                                elif black_num == 3:
                                    if empty == 1:
                                        value_list[x * 15 + y] += 100
                                    elif empty == 2:
                                        value_list[x * 15 + y] += 200
                                elif black_num >= 4:
                                    value_list[x * 15 + y] += 1000
                                empty = 0
                                for k in range(1, 5):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.status[(x + k * i) * 15 + y + k * j] == 2:
                                            white_num += 1
                                        elif self.board.status[(x + k * i) * 15 + y + k * j] == 0:
                                            empty += 1
                                            break
                                        else:
                                            break
                                    pass
                                for k in range(-1, -5, -1):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.status[(x + k * i) * 15 + y + k * j] == 1:
                                            white_num += 1
                                        elif self.board.status[(x + k * i) * 15 + y + k * j] == 0:
                                            empty += 1
                                            break
                                        else:
                                            break
                                    pass
                                if white_num == 0:
                                    value_list[x * 15 + y] += 1
                                elif white_num == 1:
                                    value_list[x * 15 + y] += 2
                                elif white_num == 2:
                                    if empty == 1:
                                        value_list[x * 15 + y] += 8
                                    elif empty == 2:
                                        value_list[x * 15 + y] += 30
                                elif white_num == 3:
                                    if empty == 1:
                                        value_list[x * 15 + y] += 50
                                    elif empty == 2:
                                        value_list[x * 15 + y] += 200
                                elif white_num >= 4:
                                    value_list[x * 15 + y] += 10000
                                empty = 0
                                black_num = 0
                                white_num = 0

        max_value = 0
        max_move = 0
        for pos in range(225):
            if max_value < value_list[pos]:
                max_move = pos
                max_value = value_list[pos]
        return max_move

    def get_move_hard(self):

        pass

    # alpha-beta
    def max_node_value(self, board, depth, player, alpha, beta):
        current_value = self.evaluate_func(board)
        if depth <= 0 or self.has_a_winner(board)[0]:
            return current_value
        best = -10000000
        for move in board.available:
            board_copy = copy.deepcopy(board)
            board_copy.update(player, move)
            temp_value = self.min_node_value(board_copy, depth - 1, player, alpha, max(best, beta))
            if temp_value > best:
                best = temp_value
            if temp_value > alpha:
                break
        return best

    def min_node_value(self, board, depth, player, alpha, beta):
        current_value = self.evaluate_func(board)
        if depth <= 0 or self.has_a_winner(board)[0]:
            return current_value

        best = 100000000

        for move in board.available:
            board_copy = copy.deepcopy(board)
            board_copy.update(3 - player, move)
            temp_value = self.max_node_value(board_copy, depth - 1, player, min(best, alpha), beta)
            if temp_value < best:
                best = temp_value
            if temp_value < beta:
                break
            pass
        return best

    def evaluate_func(self, board):
        value = 0
        return value

    # restart
    def restart(self, single_move_time=2, max_actions=1000):
        self.num_pieces = 0
        self.clear()
        self.board = Board()
        self.chessboard = PChessBoard()
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540, 450)
        self.square = PSquare()
        self.square.hide()
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100,0)
        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)

    def has_a_winner(self, board):
        """
        检查是否有玩家获胜
        """
        moved = list(set(range(225)) - set(board.available))
        if len(moved) < 5 + 2:
            return False, -1

        width = 15
        height = 15
        states = board.states
        n = 5
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                        len(set(states[i] for i in range(m, m + n))) == 1):  # 横向连成一线
                return True, player

            if (h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * width, width))) == 1):  # 竖向连成一线
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):  # 右斜向上连成一线
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):  # 左斜向下连成一线
                return True, player

        return False, -1

    # mouse move event
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super(PSingleModel, self).mousePressEvent(event)
        # if on the chess board
        if self.chessboard.left_up_x - 20.0 <= event.scenePos().x() <= self.chessboard.right_down_x + 20.0 \
                and self.chessboard.left_up_y - 20.0 <= event.scenePos().y() <= self.chessboard.right_down_y + 20.0:
            temp_col = int((event.scenePos().x() - self.chessboard.left_up_x
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            temp_row = int((event.scenePos().y() - self.chessboard.left_up_y
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            # that space has not been set piece
            if (15 * temp_row + temp_col) in self.board.available:
                self.square.show()
                self.square.setPos(self.chessboard.space
                                   * (temp_col) - 17 + 20, self.chessboard.space * (temp_row) - 17 + 20)
            else:
                self.square.hide()

    # mouse press event
    def mousePressEvent(self, event):
        super(PSingleModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton :
            print(event.scenePos().x(), event.scenePos().y())

            # if one the return button
            if 540 <= event.scenePos().x() <= 690 and 450 <= event.scenePos().y() <= 520:
                self.Signal_ChangeModel.emit(1)

            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20 \
                    and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.scenePos().x() - self.chessboard.left_up_x
                                + 0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.scenePos().y() - self.chessboard.left_up_y
                                + 0.25 * self.chessboard.space) / self.chessboard.space)
                # that space has not been set piece
                temp_move = temp_row * 15 + temp_col
                if self.board.status[temp_move] == 0:
                    # black chessman turn
                    self.num_pieces += 1
                    self.board.update((self.num_pieces + 1) % 2, temp_move)
                    temp_black_chessman = BlackChessMan(self)
                    temp_black_chessman.set_index_pos(temp_col, temp_row)
                    temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                    print("black_chess_index_pos (%d, %d)" %(temp_col, temp_row))
                    self.addItem(temp_black_chessman)
                    # TODO:whether add backup
                    #self.black_chessman_queue.append(temp_black_chessman)
                    # check for win
                    result, winner = self.has_a_winner(self.board)
                    # if black wins
                    if result:
                        print(winner, "wins")
                        self.end_game(player = 1)

                    # AI's turn
                    self.num_pieces += 1
                    # uct search for best solution
                    next_move = self.get_move_easy()
                    self.board.update((self.num_pieces + 1) % 2, next_move)
                    next_move_row, next_move_col = next_move // 15, next_move % 15
                    temp_white_chessman = WhiteChessMan(self)
                    temp_white_chessman.set_index_pos(next_move_col, next_move_row)
                    temp_white_chessman.setPos(self.chessboard.left_up_x + next_move_col * self.chessboard.space - 17,
                                                self.chessboard.left_up_y + next_move_row * self.chessboard.space - 17)
                    print("while_chess_index_pos (%d, %d)" %(next_move_col, next_move_row))
                    self.addItem(temp_white_chessman)
                    # TODO:whether add backup
                    # self.white_chessman_queue.append(temp_white_chessman)
                    # check for win
                    result, winner = self.has_a_winner(self.board)
                    # if white wins
                    if result:
                        print(winner, "wins")
                        self.end_game(player = 2)


    # win notification
    def end_game(self,player):
        # black wins
        if player == 1:
            button = QMessageBox.question(None, "胜利！"
                                          , self.tr("黑方获胜！")
                                          , QMessageBox.Ok | QMessageBox.Cancel
                                          , QMessageBox.Ok)
        # white wins
        else:
            button = QMessageBox.question(None, "胜利！"
                                          , self.tr("白方获胜！")
                                          , QMessageBox.Ok | QMessageBox.Cancel
                                          , QMessageBox.Ok)

        if button == QMessageBox.Ok:
            self.restart()
        else:
            self.restart()


def print_list(value_list):
        count = 0
        value_row_list = []
        for i in range(225):
            value_row_list.append(str(value_list[i]))
            count += 1
            if count == 15:
                print(' '.join(value_row_list))
                value_row_list = []
                count = 0
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


class BroadcastAccepter(QThread):
    Signal_recv_address_list = pyqtSignal(list, name = "Signal_recv_address_list")

    def __init__(self, parent = None):
        super(BroadcastAccepter, self).__init__(parent)
        self.get_address = {}
        self.send_address = []
        self.running = 1
        # self.broadcast_socket.setblocking(0)
        self.PORT = 1060

    def run(self):
        self.broadcast_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_recv_socket.settimeout(3)
        self.broadcast_recv_socket.bind((' ', self.PORT))
        last_len = 2
        while self.running:
            print("receiver still working")
            try:
                data, address = self.broadcast_recv_socket.recvfrom(65535)
                self.get_address[address] = (last_len + 2, data.decode('utf-8'))
            except:
                pass
            self.send_address = []
            for key in self.get_address.keys():
                if self.get_address[key][0] > 0:
                    data_list = self.get_address[key][1].split(' ')
                    self.send_address.append((data_list[0], data_list[1]))
                    self.get_address[key] = (self.get_address[key][0] - 1, self.get_address[key][1])
            last_len = len(self.send_address)

        self.broadcast_recv_socket.shutdown(2)
        self.broadcast_recv_socket.close()
        self.exit(0)

    def send_address_list(self):
        return self.send_address


class BroadcastSender(QThread):
    Signal_get_pos = pyqtSignal(int, int, name = "Signal_get_pos")

    def __init__(self, parent = None):
        super(BroadcastSender, self).__init__(parent)
        self.network = '<broadcast>'
        self.port = 1060
        self.address = socket.gethostbyname_ex(socket.gethostname())[2][-1]
        self.name = " "
        self.running = 1

    def run(self):
        self.broadcasting_address = self.name + " " + self.address
        self.broadcast_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.running:
            self.broadcast_send_socket.sendto(self.broadcasting_address.encode('utf-8'), (self.network, self.port))
            time.sleep(1)
            print("sender still working")
        self.broadcast_send_socket.shutdown(2)
        self.broadcast_send_socket.close()
        self.exit(0)


class GameLinker(QThread):
    Signal_get_message = pyqtSignal(str, name="Signal_get_message")

    def __init__(self, parent=None):
        super(GameLinker, self).__init__(parent)
        self.network = '<broadcast>'
        self.port = 1061
        self.name = None
        self.address = None
        self.running = 1
        self.is_as_client = False
        self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_threading = None

    def run(self):
        if self.is_as_client:
            self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connecting_socket.connect((self.address, self.port))
            self.recv_threading = threading.Thread(target=self.recv_msg, args=(self.connecting_socket,))
            self.recv_threading.start()
            while True and self.running:
                send_str = input()
                self.connecting_socket.send(send_str.encode('utf-8'))
            pass
        else:
            self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connecting_socket.bind((self.address, 1061))
            self.connecting_socket.listen(5)
            self.game_socket, addr = self.connecting_socket.accept()
            self.recv_threading = threading.Thread(target=self.recv_msg, args=(self.game_socket,))
            self.recv_threading.start()
            while True and self.running:
                send_str = input()
                self.game_socket.send(send_str.encode('utf-8'))
            pass
            self.game_socket.shutdown(2)
            self.game_socket.close()
        self.connecting_socket.shutdown(2)
        self.connecting_socket.close()
        self.exit(0)

    def recv_msg(self, recv_socket):
        while True:
            data = recv_socket.recv(1024).decode()
            print(data)


class PListAddress(QListWidgetItem):
    def __init__(self, name, address, parent=None):
        super(PListAddress, self).__init__(parent)
        self.name = name
        self.address = address


class PListDialog(QDialog):
    Signal_send_linker = pyqtSignal(GameLinker, name="Signal_send_linker")

    def __init__(self, parent=None):
        super(PListDialog, self).__init__(parent)
        self.setGeometry(600, 200, 600, 400)
        self.setFixedSize(600, 400)

        # component
        self.refresh_button = QPushButton()
        self.refresh_button.setFixedSize(100, 30)
        self.refresh_button.setText("刷新")
        self.refresh_button.clicked.connect(self.refresh_address_list)

        self.link_button = QPushButton()
        self.link_button.setFixedSize(100, 30)
        self.link_button.setText("连接")
        self.link_button.clicked.connect(self.connect_to_player)

        self.name_input = QLineEdit()
        self.name_input.setFixedSize(100, 20)

        self.make_room_button = QPushButton()
        self.make_room_button.setFixedSize(100, 30)
        self.make_room_button.setText("创建房间")
        self.make_room_button.clicked.connect(self.make_room)

        self.cancel_button = QPushButton()
        self.cancel_button.setFixedSize(100, 30)
        self.cancel_button.setText("退出")

        self.choices_list = QListWidget()

        # layouts
        self.main_layout = QHBoxLayout()
        self.buttons_layout = QVBoxLayout()
        self.list_layout = QVBoxLayout()

        self.buttons_layout.addWidget(self.refresh_button)
        self.buttons_layout.addWidget(self.link_button)
        self.buttons_layout.addWidget(self.name_input)
        self.buttons_layout.addWidget(self.make_room_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addStretch(7)
        self.list_layout.addWidget(self.choices_list)
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

        # socket
        self.address_list = []
        self.broadcast_recv = BroadcastAccepter()
        self.broadcast_sender = BroadcastSender()
        self.game_linker_client = GameLinker()
        self.game_linker_server = GameLinker()
        self.broadcast_recv.Signal_recv_address_list.connect(self.accept_broadcast)
        self.broadcast_recv.start()

    def accept_broadcast(self, address_list):
        print(address_list)
        self.choices_list.clear()
        for address in address_list:
            self.choices_list.addItem(address)
        pass

    def refresh_address_list(self):
        address_list = self.broadcast_recv.send_address_list()
        self.choices_list.clear()
        for address in address_list:
            temp_list_item = PListAddress(address[0], address[1])
            temp_list_item.setText(address[0])
            self.choices_list.addItem(temp_list_item)
        pass

    def make_room(self):
        name_str = self.name_input.text()
        if len(name_str) > 0:
            self.game_linker_client.running = 0
            self.link_button.setDisabled(True)
            self.broadcast_recv.running = 0
            self.make_room_button.setText("停止广播")
            self.make_room_button.clicked.disconnect(self.make_room)
            self.make_room_button.clicked.connect(self.terminate_broadcast)
            self.broadcast_sender.name = name_str
            self.broadcast_sender.running = 1
            self.broadcast_sender.start()
            self.game_linker_server.address = "59.66.137.30"
            self.game_linker_server.name = name_str
            self.game_linker_server.is_as_client = False
            self.game_linker_server.running = 1
            self.game_linker_server.start()

        else:
            QMessageBox.question(None, "提示"
                                 , self.tr("请输入昵称")
                                 , QMessageBox.Ok
                                 , QMessageBox.Ok)
        pass

    def terminate_broadcast(self):
        self.game_linker_server.running = 0
        self.link_button.setDisabled(False)
        self.broadcast_sender.running = 0
        self.make_room_button.setText("创建房间")
        self.make_room_button.clicked.disconnect(self.terminate_broadcast)
        self.make_room_button.clicked.connect(self.make_room)
        self.broadcast_recv.running = 1
        self.broadcast_recv.start()

    def connect_to_player(self):
        item_list = self.choices_list.selectedItems()
        if len(item_list) > 0:
            print("{}:{}".format(item_list[0].name, item_list[0].address))
            self.game_linker_server.running = 0
            self.game_linker_client.running = 1
            self.game_linker_client.address = item_list[0].address
            self.game_linker_client.name = "myself"
            self.game_linker_client.is_as_client = True
            self.game_linker_client.start()
        pass


# online model
class POnlineModel(PModel):
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent: 'PModel' = None):
        super(POnlineModel, self).__init__(parent)
        # init UI
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        self.board = Board()

        # stack for black piece and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540, 0)

        # cursor square
        self.square = PSquare()

        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)
        self.square.hide()

        # game status
        self.receiving_broadcast = True
        self.game_start = False
        self.game_end = False

        self.list_window = PListDialog()
        self.list_window.cancel_button.clicked.connect(self.quit_model)
        self.list_window.setModal(True)

        self.list_window.show()
        self.list_window.Signal_send_linker.connect(self.get_linker)
        self.game_linker = None

    def get_linker(self, game_linker):
        self.game_linker = game_linker

    def game_start(self):
        self.chessboard.show()
        self.returnLabel.show()
        self.square.show()
        pass

    def quit_model(self):
        self.list_window.broadcast_recv.running = 0
        self.list_window.broadcast_sender.running = 0
        self.list_window.hide()
        self.Signal_ChangeModel.emit(1)
        pass

    # mouse move event
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super(POnlineModel, self).mousePressEvent(event)
        # if on the chess board
        if self.chessboard.left_up_x - 20.0 <= event.scenePos().x() <= self.chessboard.right_down_x + 20.0 \
                and self.chessboard.left_up_y - 20.0 <= event.scenePos().y() <= self.chessboard.right_down_y + 20.0\
                and self.game_start:
            temp_col = int((event.scenePos().x() - self.chessboard.left_up_x
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            temp_row = int((event.scenePos().y() - self.chessboard.left_up_y
                            + 0.25 * self.chessboard.space) / self.chessboard.space)
            # that space has not been set piece
            if (15 * temp_row + temp_col) in self.board.available:
                self.square.show()
                self.square.setPos(self.chessboard.space
                                   * (temp_col) - 17 + 20, self.chessboard.space * (temp_row) - 17 + 20)
            else:
                self.square.hide()
        elif self.receiving_broadcast:

            pass

    # mouse press event
    def mousePressEvent(self, event):
        super(POnlineModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton and self.game_start:
            print(event.scenePos().x(), event.scenePos().y())
            # if one the return button
            if 540 <= event.scenePos().x() <= 690 and 0 <= event.scenePos().y() <= 70:
                self.Signal_ChangeModel.emit(3)
            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20 \
                    and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.scenePos().x() - self.chessboard.left_up_x +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.scenePos().y() - self.chessboard.left_up_y +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                # that space has not been set piece
                if self.situation_matrix[temp_row][temp_col] == 0:
                    # black chessman turn
                    if self.num_pieces % 2 == 0:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 1
                        temp_black_chessman = BlackChessMan(self)
                        temp_black_chessman.set_index_pos(temp_col, temp_row)
                        temp_black_chessman.setPos(
                            self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                            self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("black_chess_index_pos (%d, %d)" % (temp_col, temp_row))
                        self.addItem(temp_black_chessman)
                        self.black_chessman_queue.append(temp_black_chessman)
                        # check for win
                        result = check_win_black(self.situation_matrix)
                        # if black wins
                        if result == 1:
                            print("black wins")
                            self.restart()
                    else:
                        self.num_pieces += 1
                        self.situation_matrix[temp_row][temp_col] = 2
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(temp_col, temp_row)
                        temp_white_chessman.setPos(
                            self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                            self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" % (temp_col, temp_row))
                        self.addItem(temp_white_chessman)
                        self.white_chessman_queue.append(temp_white_chessman)
                        # check for win
                        result = check_win_white(self.situation_matrix)
                        # if white wins
                        if result == 2:
                            print("white wins")
                            self.restart()
            pass
        elif event.button() == Qt.LeftButton and self.receiving_broadcast:
            if 100.0 <= event.scenePos().x() <= 200.0:

                pass