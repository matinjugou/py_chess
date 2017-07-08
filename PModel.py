from PItems import *
from collections import deque
from PyQt5.QtCore import *
import PyQt5.QtGui as QtGui
import numpy as np
import copy as copy
import socket
import time
import threading
import fileinput


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
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent = None):
        super(PMultipleModel, self).__init__(parent)
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        self.board = Board()
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

        # add the item
        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.square)
        self.addItem(self.saveLabel)
        self.addItem(self.returnLabel)
        self.addItem(self.undoLabel)

        # chose the level
        customMsgBox = QMessageBox(None)
        customMsgBox.setWindowTitle("读取存档")
        archiveButton = customMsgBox.addButton(self.tr("读档"),
                                            QMessageBox.ActionRole)
        newgameButton = customMsgBox.addButton(self.tr("新游戏"),
                                              QMessageBox.ActionRole)

        customMsgBox.setText(self.tr("读取上一盘的存档 or 开始新游戏"))
        customMsgBox.exec_()

        button = customMsgBox.clickedButton()
        if button == archiveButton:
            self.ReadArchive()
            # add the load file writer
            self.fp = open("resources//doc//multiple.txt", 'a')
        elif button == newgameButton:
            # add the load file writer
            self.fp = open("resources//doc//multiple.txt", 'w')
        else:
            pass

        pass

    # read the load file
    def ReadArchive(self):
        file_reader = open("resources//doc//multiple.txt",'r')
        while 1:
            line = file_reader.readline()
            if not line:# end of the file
                break
            else:
                if len(line) > 3:# line can not be a '\n'
                    temp_type, temp_row, temp_col = line.split(' ')
                    temp_type = int(temp_type)
                    temp_row = int(temp_row)
                    temp_col = int(temp_col)
                    temp_move = temp_row * 15 + temp_col
                    if temp_type == 1:# black chessman
                        self.num_pieces += 1
                        # self.situation_matrix[temp_row][temp_col] = 1
                        self.board.update((self.num_pieces + 1) % 2, temp_move)
                        temp_black_chessman = BlackChessMan(self)
                        temp_black_chessman.set_index_pos(temp_row, temp_col)
                        temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                   self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)

                        print("black_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                        self.addItem(temp_black_chessman)
                        self.black_chessman_queue.append(temp_black_chessman)
                    else:# white chessman
                        self.num_pieces += 1
                        # self.situation_matrix[temp_row][temp_col] = 2
                        self.board.update((self.num_pieces + 1) % 2, temp_move)
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(temp_row, temp_col)
                        temp_white_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                   self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                        self.addItem(temp_white_chessman)
                        self.white_chessman_queue.append(temp_white_chessman)

    # restart
    def restart(self):
        self.black_chessman_queue.clear()
        self.white_chessman_queue.clear()
        self.num_pieces = 0
        self.clear()
        self.board = Board()
        # self.situation_matrix = [([0] * 15) for i in range(0, 15)]

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

        # Save label
        self.saveLabel = PSave()
        self.saveLabel.setPos(540,310)

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
            temp_move = temp_row * 15 + temp_col
            # that space has not been set piece
            if temp_move in self.board.available:
            # if self.situation_matrix[temp_row][temp_col] == 0:
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
                # remove the last line in multiple.txt
                self.fp.close()
                f = fileinput.input("resources//doc//multiple.txt" , inplace = True)
                for line in f:
                    if f.filelineno() != self.num_pieces and len(line) > 3:
                        print(line,end = '')
                    else:
                        pass
                f.close()
                self.fp = open("resources//doc//multiple.txt", 'a')
                # other undo operation
                temp_row, temp_col = self.black_chessman_queue[-1].index_pos
                temp_move = temp_row * 15 + temp_col
                print('{},{}'.format(temp_row, temp_col))
                self.removeItem(self.black_chessman_queue.pop())
                # self.situation_matrix[temp_row][temp_col] = 0
                self.board.available.append(temp_move)
                self.board.available.sort()
                self.board.states[temp_move] = -1
                self.board.states[temp_move] = -1
                self.num_pieces -= 1
            # if white just set a chessman
            else:
                # remove the last line in multiple.txt
                self.fp.close()
                f = fileinput.input("resources//doc//multiple.txt" , inplace = True)
                for line in f:
                    if f.filelineno() != self.num_pieces and len(line) > 3:
                        print(line,end = '')
                    else:
                        pass
                f.close()
                self.fp = open("resources//doc//multiple.txt", 'a')
                # other important operation
                temp_row , temp_col = self.white_chessman_queue[-1].index_pos
                temp_move = temp_row * 15 + temp_col
                print('{},{}'.format(temp_row, temp_col))
                self.removeItem(self.white_chessman_queue.pop())
                # self.situation_matrix[temp_row][temp_col] = 0
                self.board.available.append(temp_move)
                self.board.available.sort()
                self.board.states[temp_move] = -1
                self.board.states[temp_move] = -1
                self.num_pieces -= 1

    # mouse press event
    def mousePressEvent(self, event):
        super(PMultipleModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton:
            print(event.scenePos().x(), event.scenePos().y())

            # if on the save button
            if 540 <= event.scenePos().x() <= 690 and 310 <= event.scenePos().y() <= 380:
                pass

            # if on the undo button
            if 540 <= event.scenePos().x() <= 690 and 380 <= event.scenePos().y() <= 440:
                self.Undo()

            # if on the return button
            if 540 <= event.scenePos().x() <= 690 and 450 <= event.scenePos().y() <= 520:
                # turn off the file reader
                self.fp.close()
                # turn back to start menu
                self.Signal_ChangeModel.emit(1)

            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20\
                    and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.scenePos().x() - self.chessboard.left_up_x +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.scenePos().y() - self.chessboard.left_up_y +
                                0.25 * self.chessboard.space) / self.chessboard.space)
                temp_move = temp_row * 15 + temp_col
                # that space has not been set piece
                if temp_move in self.board.available:
                # if self.situation_matrix[temp_row][temp_col] == 0:
                    # black chessman turn
                    if self.num_pieces % 2 == 0:
                        self.num_pieces += 1
                        # self.situation_matrix[temp_row][temp_col] = 1
                        self.board.update((self.num_pieces + 1) % 2, temp_move)
                        temp_black_chessman = BlackChessMan(self)
                        temp_black_chessman.set_index_pos(temp_row, temp_col)
                        temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)

                        print("black_chess_index_pos (%d, %d)" %(temp_row, temp_col))
                        self.addItem(temp_black_chessman)
                        self.black_chessman_queue.append(temp_black_chessman)
                        # check for win
                        result, winner = has_a_winner(self.board)
                        # if black wins
                        if result:
                            print("black wins")
                            self.end_game(player = 1)
                        else:
                            # write the file
                            self.fp.write('1' + ' '+str(temp_row) + ' '+ str(temp_col) + '\n')

                    else:
                        self.num_pieces += 1
                        # self.situation_matrix[temp_row][temp_col] = 2
                        self.board.update((self.num_pieces + 1) % 2, temp_move)
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(temp_row, temp_col)
                        temp_white_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" %(temp_row, temp_col))
                        self.addItem(temp_white_chessman)
                        self.white_chessman_queue.append(temp_white_chessman)
                        # check for win
                        result, winner = has_a_winner(self.board)
                        # if white wins
                        if result:
                            print("white wins")
                            self.end_game(player = 2)
                        else:
                            # write the file
                            self.fp.write('2' + ' ' + str(temp_row) + ' ' + str(temp_col) + '\n')

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
        self.computer_player = 1
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
    def get_move_hard(self):
        empty = 0
        black_num = 0
        white_num = 0
        value_list = np.zeros(225)
        for x in range(15):
            for y in range(15):
                if self.board.states[x * 15 + y] == -1:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                for k in range(1, 5):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.states[(x + k * i) * 15 + y + k * j] == 0:
                                            black_num += 1
                                        elif self.board.states[(x + k * i) * 15 + y + k * j] == -1:
                                            empty += 1
                                            break
                                        else:
                                            break
                                for k in range(-1, -5, -1):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.states[(x + k * i) * 15 + y + k * j] == 0:
                                            black_num += 1
                                        elif self.board.states[(x + k * i) * 15 + y + k * j] == -1:
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
                                        if self.board.states[(x + k * i) * 15 + y + k * j] == 1:
                                            white_num += 1
                                        elif self.board.states[(x + k * i) * 15 + y + k * j] == -1:
                                            empty += 1
                                            break
                                        else:
                                            break
                                    pass
                                for k in range(-1, -5, -1):
                                    if 0 <= x + k * i <= 14 and 0 <= y + k * j <= 14:
                                        if self.board.states[(x + k * i) * 15 + y + k * j] == 1:
                                            white_num += 1
                                        elif self.board.states[(x + k * i) * 15 + y + k * j] == -1:
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

    def get_move_easy(self):
        value_list = []
        for move in self.board.available:
            board_copy = copy.deepcopy(self.board)
            board_copy.update(self.computer_player, move)
            value_list.append(self.max_node_value(board_copy, 0, self.computer_player, 1000000, -1000000))
        pass
        max_value = -1000000
        max_index = 0
        for i in range(len(value_list)):
            if value_list[i] > max_value:
                max_value = value_list[i]
                max_index = i
        return self.board.available[max_index]

    # alpha-beta
    def max_node_value(self, board, depth, player, alpha, beta):
        current_value = getScore(board, player)
        if depth <= 0 or has_a_winner(board)[0]:
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
        current_value = getScore(board, player)
        if depth <= 0 or has_a_winner(board)[0]:
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
                if temp_move in self.board.available:
                    # black chessman turn
                    self.num_pieces += 1
                    self.board.update((self.num_pieces + 1) % 2, temp_move)
                    temp_black_chessman = BlackChessMan(self)
                    temp_black_chessman.set_index_pos(temp_col, temp_row)
                    temp_black_chessman.setPos(self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                                self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                    print("black_chess_index_pos (%d, %d)" %(temp_col, temp_row))
                    self.addItem(temp_black_chessman)
                    # check for win
                    result, winner = has_a_winner(self.board)
                    # if black wins
                    if result:
                        print(winner, "wins")
                        self.end_game(player = 1)
                    else:
                        # AI's turn
                        self.num_pieces += 1
                        # search for best solution
                        if self.level == 1:
                            next_move = self.get_move_easy()
                        else:
                            next_move = self.get_move_hard()
                        self.board.update((self.num_pieces + 1) % 2, next_move)
                        next_move_row, next_move_col = next_move // 15, next_move % 15
                        temp_white_chessman = WhiteChessMan(self)
                        temp_white_chessman.set_index_pos(next_move_col, next_move_row)
                        temp_white_chessman.setPos(self.chessboard.left_up_x + next_move_col * self.chessboard.space - 17,
                                                    self.chessboard.left_up_y + next_move_row * self.chessboard.space - 17)
                        print("while_chess_index_pos (%d, %d)" %(next_move_col, next_move_row))
                        self.addItem(temp_white_chessman)
                        # check for win
                        result, winner = has_a_winner(self.board)
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


def getScore(board, player):
    moved = list(set(range(225)) - set(board.available))
    width = board.width
    total_value = 0
    states = board.states
    n = 5
    for m in moved:
        h = m // width
        w = m % width
        states_list = list(states[i] for i in range(h * 15, h * 15 + 15) if 0 <= i < 225)
        total_value += evaluate(states_list, player)

        states_list = list(states[i] for i in range(w, 15 * 15 + w, width) if 0 <= i < 225)
        total_value += evaluate(states_list, player)

        states_list = []
        point_list = []
        pin = m % 16
        point = m
        while point % 16 <= pin and point >= 0:
            point_list.append(point)
            point -= 16
        point = m + 16
        while point % 16 > pin and point < 225:
            point_list.append(point)
            point += 16
        point_list.sort()
        states_list = list(states[i] for i in point_list)
        total_value += evaluate(states_list, player)

        states_list = []
        point_list = []
        pin = m % 14
        point = m
        while point % 14 >= pin and point > 0:
            point_list.append(point)
            point -= 14
        point = m + 14
        while point % 14 < pin and point < 225:
            point_list.append(point)
            point += 14
        point_list.sort()
        states_list = list(states[i] for i in point_list)
        total_value += evaluate(states_list, player)
        pass
    return total_value


def evaluate(states_list, player):
    list_str = ""
    for state in states_list:
        if state == player:
            list_str += "1"
        elif state == 1 - player:
            list_str += "2"
        else:
            list_str += "0"
    list_str = "3" + list_str + "3"
    tot_value = 0
    if "010" in list_str:
        tot_value += 10
    if "210" or "310" or "012" or "013" in list_str:
        tot_value += 5
    if "212" or "213" or "312" in list_str:
        tot_value -= 1
    if "0110" in list_str:
        tot_value += 100
    if "2110" or "3110" or "0112" or "0113" in list_str:
        tot_value += 50
    if "2112" or "2113" or "3112" in list_str:
        tot_value -= 10
    if "01110" in list_str:
        tot_value += 500
    if "21110" or "31110" or "01112" or "01113" in list_str:
        tot_value += 300
    if "21112" or "21113" or "31112" in list_str:
        tot_value -= 200
    if "011110" in list_str:
        tot_value += 100000
    if "211110" or "311110" or "011112" or "011113" in list_str:
        tot_value += 490
    if "211112" or "211113" or "311112" in list_str:
        tot_value -= 300
    if "11111" in list_str and "111111" not in list_str:
        tot_value += 100000

    if "020" in list_str:
        tot_value -= 15
    if "120" or "320" or "021" or "023" in list_str:
        tot_value -= 10
    if "121" or "123" or "321" in list_str:
        tot_value += 5
    if "0220" in list_str:
        tot_value -= 105
    if "1220" or "3220" or "0221" or "0223" in list_str:
        tot_value -= 55
    if "1221" or "1223" or "3221" in list_str:
        tot_value += 15
    if "02220" in list_str:
        tot_value -= 510
    if "12220" or "32220" or "02221" or "02223" in list_str:
        tot_value -= 410
    if "12221" or "12223" or "32221" in list_str:
        tot_value += 260
    if "022220" in list_str:
        tot_value -= 10010
    if "122220" or "322220" or "022221" or "022223" in list_str:
        tot_value -= 500
    if "122221" or "122223" or "322221" in list_str:
        tot_value += 260
    if "22222" in list_str and "22222" not in list_str:
        tot_value -= 10010
    return tot_value


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


def has_a_winner(board):
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
        self.broadcast_recv_socket.bind(('0.0.0.0', self.PORT))
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
    Signal_send_request = pyqtSignal()

    def __init__(self, parent=None):
        super(GameLinker, self).__init__(parent)
        self.network = '<broadcast>'
        self.port = 1061
        self.name = None
        self.address = None
        self.running = 1
        self.is_as_client = False
        self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_socket = None
        self.recv_threading = None

    def run(self):
        if self.is_as_client:
            self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connecting_socket.connect((self.address, self.port))
            self.game_socket = self.connecting_socket
            self.Signal_send_request.emit()
        else:
            self.connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connecting_socket.bind((self.address, 1061))
            self.connecting_socket.listen(5)
            self.game_socket, addr = self.connecting_socket.accept()
            self.Signal_send_request.emit()

    def get_info(self):
        return self.connecting_socket, self.game_socket, self.is_as_client


class PListAddress(QListWidgetItem):
    def __init__(self, name, address, parent=None):
        super(PListAddress, self).__init__(parent)
        self.name = name
        self.address = address


class PListDialog(QDialog):
    Signal_send_linker = pyqtSignal(GameLinker, name="Signal_send_linker")
    Signal_quit_model = pyqtSignal()

    def __init__(self, parent=None):
        super(PListDialog, self).__init__(parent)
        self.setGeometry(600, 200, 600, 400)
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

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

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.Signal_quit_model.emit()
        self.broadcast_sender.running = 0
        self.broadcast_recv.running = 0
        event.accept()
        pass

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
            self.game_linker_server.address = socket.gethostbyname_ex(socket.gethostname())[2][-1]
            self.game_linker_server.name = name_str
            self.game_linker_server.is_as_client = False
            self.game_linker_server.running = 1
            self.game_linker_server.start()
            self.Signal_send_linker.emit(self.game_linker_server)

        else:
            QMessageBox.question(None, "提示"
                                 , self.tr("请输入昵称")
                                 , QMessageBox.Ok
                                 , QMessageBox.Ok)
        pass

    def close_broadcast(self):
        self.broadcast_sender.running = 0
        self.broadcast_recv.running = 0
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
            self.Signal_send_linker.emit(self.game_linker_client)
        pass


# online model
class POnlineModel(PModel):
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")
    Signal_AddChessman = pyqtSignal(int, int, name="Signal_AddChessman")

    def __init__(self, parent: 'PModel' = None):
        super(POnlineModel, self).__init__(parent)
        # init UI
        self.chessboard = PChessBoard()
        self.chessboard.setPos(0, 0)
        self.board = Board()
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100, 0)

        # stack for black piece and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540, 450)

        # undo label
        self.undoLabel = PUndo()
        self.undoLabel.setPos(540, 380)

        # cursor square
        self.square = PSquare()

        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)
        self.addItem(self.undoLabel)
        self.square.hide()

        # game status
        self.receiving_broadcast = True
        self.game_start = False
        self.game_end = False

        self.list_window = PListDialog()
        self.list_window.cancel_button.clicked.connect(self.quit_model)
        self.list_window.Signal_quit_model.connect(self.quit_model)
        self.list_window.setModal(True)

        self.list_window.show()
        self.list_window.Signal_send_linker.connect(self.get_linker)
        self.recv_threading = None
        self.connecting_socket = None
        self.game_socket = None
        self.game_linker = None
        self.is_as_client = False
        self.Signal_AddChessman.connect(self.add_chessman)

    def restart(self):
        self.black_chessman_queue.clear()
        self.white_chessman_queue.clear()
        self.num_pieces = 0
        self.clear()
        self.board = Board()
        self.supplement = PPicture_Supplement()
        self.supplement.setPos(100, 0)

        self.chessboard = PChessBoard()

        self.returnLabel = PReturn()
        self.returnLabel.setPos(540, 450)

        self.square = PSquare()
        self.square.hide()

        # undo label
        self.undoLabel = PUndo()
        self.undoLabel.setPos(540, 380)

        self.addItem(self.supplement)
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)
        self.addItem(self.undoLabel)
        self.square.hide()

    def add_chessman(self, temp_row, temp_col):
        if not self.is_as_client and self.num_pieces % 2 == 1:
            temp_move = temp_row * 15 + temp_col
            if temp_move in self.board.available:
                # black chessman turn
                self.num_pieces += 1
                temp_white_chessman = WhiteChessMan(self)
                temp_white_chessman.set_index_pos(temp_row, temp_col)
                temp_white_chessman.setPos(
                    self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                print("black_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                self.addItem(temp_white_chessman)
                self.white_chessman_queue.append(temp_white_chessman)
                self.board.update(self.num_pieces % 2, temp_move)
                # check for win
                result, winner = has_a_winner(self.board)
                # if black wins
                if result == 1:
                    print("black wins")
                    self.end_game(winner)

        elif self.is_as_client and self.num_pieces % 2 == 0:
            temp_move = temp_row * 15 + temp_col
            if temp_move in self.board.available:
                # black chessman turn
                self.num_pieces += 1
                temp_black_chessman = BlackChessMan(self)
                temp_black_chessman.set_index_pos(temp_row, temp_col)
                temp_black_chessman.setPos(
                    self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                    self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                print("black_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                self.addItem(temp_black_chessman)
                self.black_chessman_queue.append(temp_black_chessman)
                self.board.update(self.num_pieces % 2, temp_move)
                # check for win
                result, winner = has_a_winner(self.board)
                # if black wins
                if result == 1:
                    print("black wins")
                    self.end_game(winner)
            pass
        pass

    def get_move_from_net(self):
        while True:
            data = self.game_socket.recv(1024).decode('utf-8')
            if data != "exit":
                data_list = data.split(',')
                temp_row = int(data_list[0])
                temp_col = int(data_list[1])
                self.Signal_AddChessman.emit(temp_row, temp_col)
            else:
                break
        self.quit_game()
        pass

    def get_socket(self):
        self.connecting_socket, self.game_socket, self.is_as_client = self.game_linker.get_info()
        self.game_linker.exit(0)
        self.list_window.close_broadcast()
        self.list_window.hide()
        self.game_start = True
        self.receiving_broadcast = False
        self.recv_threading = threading.Thread(target=self.get_move_from_net)
        self.recv_threading.start()
        pass

    def get_linker(self, game_linker):
        self.game_linker = game_linker
        self.game_linker.Signal_send_request.connect(self.get_socket)

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

    def quit_game(self):
        self.game_socket.close()
        if not self.is_as_client:
            self.connecting_socket.close()
        self.Signal_ChangeModel.emit(1)

    # mouse press event
    def mousePressEvent(self, event):
        super(POnlineModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton and self.game_start:
            print(event.scenePos().x(), event.scenePos().y())
            # if one the return button
            if 540 <= event.scenePos().x() <= 690 and 450 <= event.scenePos().y() <= 520:
                self.game_socket.send("exit".encode('utf-8'))
                self.quit_game()
            # if on the chess board
            if not self.is_as_client and self.num_pieces % 2 == 0:
                if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20 \
                        and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                    temp_col = int((event.scenePos().x() - self.chessboard.left_up_x +
                                    0.25 * self.chessboard.space) / self.chessboard.space)
                    temp_row = int((event.scenePos().y() - self.chessboard.left_up_y +
                                    0.25 * self.chessboard.space) / self.chessboard.space)
                    temp_move = temp_row * 15 + temp_col
                    if temp_move in self.board.available:
                        # black chessman turn
                            self.num_pieces += 1
                            temp_black_chessman = BlackChessMan(self)
                            temp_black_chessman.set_index_pos(temp_row, temp_col)
                            temp_black_chessman.setPos(
                                self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                            print("black_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                            self.addItem(temp_black_chessman)
                            self.black_chessman_queue.append(temp_black_chessman)
                            self.board.update(self.num_pieces % 2, temp_move)
                            # check for win
                            result, winner = has_a_winner(self.board)
                            # if black wins
                            if result == 1:
                                print("black wins")
                                self.end_game(winner)
                            send_str = str(temp_row) + ',' + str(temp_col)
                            self.game_socket.send(send_str.encode('utf-8'))
            elif self.is_as_client and self.num_pieces % 2 == 1:
                if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20 \
                        and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                    temp_col = int((event.scenePos().x() - self.chessboard.left_up_x +
                                    0.25 * self.chessboard.space) / self.chessboard.space)
                    temp_row = int((event.scenePos().y() - self.chessboard.left_up_y +
                                    0.25 * self.chessboard.space) / self.chessboard.space)
                    temp_move = temp_row * 15 + temp_col
                    if temp_move in self.board.available:
                        # black chessman turn
                            self.num_pieces += 1
                            temp_white_chessman = WhiteChessMan(self)
                            temp_white_chessman.set_index_pos(temp_row, temp_col)
                            temp_white_chessman.setPos(
                                self.chessboard.left_up_x + temp_col * self.chessboard.space - 17,
                                self.chessboard.left_up_y + temp_row * self.chessboard.space - 17)
                            print("black_chess_index_pos (%d, %d)" % (temp_row, temp_col))
                            self.addItem(temp_white_chessman)
                            self.white_chessman_queue.append(temp_white_chessman)
                            self.board.update(self.num_pieces % 2, temp_move)
                            # check for win
                            result, winner = has_a_winner(self.board)
                            # if black wins
                            if result == 1:
                                print("black wins")
                                self.end_game(winner)
                            send_str = str(temp_row) + ',' + str(temp_col)
                            self.game_socket.send(send_str.encode('utf-8'))
                pass

    # win notification
    def end_game(self, player):
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