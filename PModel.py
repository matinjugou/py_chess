from PChessBoard import *
from collections import deque
from PStartMenuView import *
import time as time
import copy as copy
from random import choice
from math import log, sqrt


class PModel(QGraphicsScene):
    def __init__(self, parent = None):
        super(PModel, self).__init__(parent)
    pass


class PStartMenu(PModel):
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, parent = None):
        super(PStartMenu, self).__init__(parent)
        # TODO:create a startmenu including single player and multiple player
        self.startMenu = PStartMenuBackGround()
        self.startMenu.setPos(0,0)

        # multiple label
        self.multipleLabel = PStartMenu_Multiple()
        self.multipleLabel.setPos(400,30)

        # machine label
        self.machineLabel = PStartMenu_Machine()
        self.machineLabel.setPos(400,120)
        
        # add the item
        self.addItem(self.startMenu)
        self.addItem(self.machineLabel)
        self.addItem(self.multipleLabel)
    pass

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print(event.scenePos().x(),event.scenePos().y())
        if 400.0 <= event.scenePos().x() <= 680.0:
            if 30.0 <= event.scenePos().y() <= 110.0:
                self.Signal_ChangeModel.emit(2)
            elif 120.0 <= event.scenePos().y() <= 200.0:
                self.Signal_ChangeModel.emit(1)
            pass

class PMultipleModel(PModel):
    # signal to emit
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

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

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540,0)

        # cursor square
        self.square = PSquare()

        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)
        pass

    # restart
    def restart(self):
        self.black_chessman_queue.clear()
        self.white_chessman_queue.clear()
        self.num_pieces = 0
        self.clear()
        self.chessboard = PChessBoard()
        self.returnLabel = PReturn()
        self.square = PSquare()
        self.square.hide()
        self.returnLabel.setPos(540,0)
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)

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


    # mouse press event
    def mousePressEvent(self, event):
        super(PMultipleModel, self).mousePressEvent(event)
        print(event.scenePos())
        if event.button() == Qt.LeftButton:
            print(event.scenePos().x(), event.scenePos().y())
            # if one the return button
            if 540 <= event.scenePos().x() <= 690 and 0 <= event.scenePos().y() <= 70:
                self.Signal_ChangeModel.emit(3)
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

            pass


class Board(object):
    """
    board for game
    """

    def __init__(self):
        self.width = 15
        self.height = 15
        self.states = {} # board states, key:(player, move), value: piece type
        self.n_in_row = 5 # need how many pieces in a row to win
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
# TODO:add a function by which player can choose that AI go first
class PSingleModel(PModel):
    Signal_ChangeModel = pyqtSignal(int, name="Signal_ChangeModel")

    def __init__(self, single_move_time=2, max_actions = 1000, parent:PModel = None):
        super(PSingleModel, self).__init__()
        self.scene = QGraphicsScene()
        self.chessboard = PChessBoard()

        self.chessboard.setPos(0, 0)
        # represent the statu of the chessboard, 0 standing for nothing, 1 standing for black
        # chessman, 2 standing for white
        # TODO:change the 2 dimensions chessboard into 1 dimension totally to lessen search time



        self.available = list(range(225))

        # TODO:to dicide whether we need following statements
        # stack for black chess and white chess
        # self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        # self.black_chessman_queue = deque()
        # self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0

        # cursor square
        self.square = PSquare()

        # return label
        self.returnLabel = PReturn()
        self.returnLabel.setPos(540,0)

        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)

        # some uct arguments
        self.plays = {}
        self.wins = {}
        self.plays_rave = {}
        self.wins_rave = {}

        self.board = Board()
        self.calculation_time = float(single_move_time)
        self.max_actions = max_actions
        self.confident = 1.96
        self.max_depth = 1
        self.equivalence = 10000
        self.state = [0 for i in range(225)]
        pass

    # restart
    def restart(self,single_move_time=2, max_actions = 1000):
        self.num_pieces = 0
        self.clear()

        # some uct arguments
        self.plays = {}
        self.wins = {}
        self.plays_rave = {}
        self.wins_rave = {}

        self.board = Board()
        self.calculation_time = float(single_move_time)
        self.max_actions = max_actions
        self.confident = 1.96
        self.max_depth = 1
        self.equivalence = 10000
        self.state = [0 for i in range(225)]

        self.available = list(range(225))
        self.chessboard = PChessBoard()
        self.returnLabel = PReturn()
        self.square = PSquare()
        self.square.hide()
        self.returnLabel.setPos(540,0)
        self.addItem(self.chessboard)
        self.addItem(self.returnLabel)
        self.addItem(self.square)

    # Standard UCT functions
    def get_action(self):
        next_move_x = 0
        next_move_y = 0
        if len(self.board.available) == 1:
            return self.board.move_to_location(self.board.available[0])
        self.plays = {}
        self.wins = {}
        self.plays_rave = {}
        self.wins_rave = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            board_copy = copy.deepcopy(self.board)
            self.run_simulation(board_copy, self.num_pieces % 2)
            simulations += 1
        print("total simulations=", simulations)

        move = self.select_one_move(self.num_pieces % 2)
        location = self.board.move_to_location(move)
        print('Maximum depth searched:', self.max_depth)

        print("AI move: %d,%d\n" % (location[0], location[1]))

        return move

    # TODO:Trans these codes into my framework

    def run_simulation(self, board, player):
        plays = self.plays
        wins = self.wins

        expand = True
        visited_states = set()
        winner = -1
        plays_rave = self.plays_rave
        wins_rave = self.wins_rave
        available = board.available
        
        # Simulation
        for t in range(1, self.max_actions + 1):
            if all(plays.get((player, move)) for move in available):
                value, move = max(
                    ((1 - sqrt(self.equivalence / (3 * plays_rave[move] + self.equivalence))) * (
                    wins[(player, move)] / plays[(player, move)]) +
                     sqrt(self.equivalence / (3 * plays_rave[move] + self.equivalence)) * (
                     wins_rave[move][player] / plays_rave[move]) +
                     sqrt(self.confident * log(plays_rave[move]) / plays[(player, move)]), move)
                    for move in available)  # UCT RAVE  公式: (1-beta)*MC + beta*AMAF + UCB
            else:
                adjacent = []
                if len(available) > 5:
                    adjacent = self.adjacent_moves(board, player, plays)

                if len(adjacent):
                    move = choice(adjacent)
                else:
                    peripherals = []
                    for move in available:
                        if not plays.get((player, move)):
                            peripherals.append(move)
                    move = choice(peripherals)

            board.update(player, move)

            # Expand
            if expand and (player, move) not in plays:
                expand = False
                plays[(player, move)] = 0
                wins[(player, move)] = 0
                if move not in plays_rave:
                    plays_rave[move] = 0
                if move in wins_rave:
                    wins_rave[move][player] = 0
                else:
                    wins_rave[move] = {player : 0}
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, move))

            is_full = not len(available)
            win, winner = self.has_a_winner(board)
            if is_full or win:
                break

            player = (player + 1) % 2
        # Back-propagation
        for player, move in visited_states:
            if (player, move) in plays:
                plays[(player, move)] += 1
                if player == winner:
                    wins[(player, move)] += 1
            if move in plays_rave:
                plays_rave[move] += 1
                if winner in wins_rave[move]:
                    wins_rave[move][winner] += 1
        pass

    def has_a_winner(self, board):
        moved = list(set(range(board.width * board.height)) - set(board.available))
        if len(moved) < 5 + 2:
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = 5
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                        len(set(states[i] for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                        len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def select_one_move(self, player):
        percent_wins, move = max(
            (self.wins.get((player, move), 0) /
             self.plays.get((player, move), 1),
             move)
            for move in self.board.available)  # 选择胜率最高的着法
        return move

    def adjacent_moves(self, board, player, plays):
        moved = list(set(range(225)) - set(board.available))
        adjacent = set()
        width = 15
        height = 15

        for m in moved:
            h = m // width
            w = m % width
            if w < width - 1:
                adjacent.add(m + 1)  # right
            if w > 0:
                adjacent.add(m - 1)  # left
            if h < height - 1:
                adjacent.add(m + width)  # upper
            if h > 0:
                adjacent.add(m - width)  # lower
            if w < width - 1 and h < height - 1:
                adjacent.add(m + width + 1)  # upper right
            if w > 0 and h < height - 1:
                adjacent.add(m + width - 1)  # upper left
            if w < width - 1 and h > 0:
                adjacent.add(m - width + 1)  # lower right
            if w > 0 and h > 0:
                adjacent.add(m - width - 1)  # lower left

        adjacent = list(set(adjacent) - set(moved))
        for move in adjacent:
            if plays.get((player, move)):
                adjacent.remove(move)
        return adjacent



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
        if event.button() == Qt.LeftButton:
            print(event.scenePos().x(), event.scenePos().y())
            # if one the return button
            if event.scenePos().x() >= 540 and event.scenePos().x() <= 690 and event.scenePos().y() <= 70  and event.scenePos().y() >= 0:
                self.Signal_ChangeModel.emit(3)
            # if on the chess board
            if self.chessboard.left_up_x - 20 <= event.scenePos().x() <= self.chessboard.right_down_x + 20 and self.chessboard.left_up_y - 20 <= event.scenePos().y() <= self.chessboard.right_down_y + 20:
                temp_col = int((event.scenePos().x() - self.chessboard.left_up_x + 0.25 * self.chessboard.space) / self.chessboard.space)
                temp_row = int((event.scenePos().y() - self.chessboard.left_up_y + 0.25 * self.chessboard.space) / self.chessboard.space)
                # that space has not been set piece
                temp_move = temp_row * 15 + temp_col
                if temp_row in self.board.available:
                    # black chessman turn
                    self.num_pieces += 1
                    self.board.update(self.num_pieces % 2, temp_move)
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
                        self.restart()


                    # AI's turn
                    self.num_pieces += 1
                    # uct search for best solution
                    next_move = self.get_action()
                    next_move_row, next_move_col = self.board.move_to_location(next_move)
                    self.board.update(self.num_pieces % 2, next_move)
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
                        self.restart()

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
