from PChessBoard import *
from collections import deque
import time as time
import copy as copy

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


# the model in which people play with AI.
# temporarily, we rule it that AI go first using white chessman
# TODO:add a function by which player can choose that AI go first
class PSingleModel(PModel):
    a = pyqtSignal(int, name = "a")
    a.emit(5)
    def __init__(self, single_move_time=5, max_actions = 1000, parent:PModel = None):
        super(PSingleModel, self).__init__()
        self.scene = QGraphicsScene()
        self.chessboard = PChessBoard()

        self.chessboard.setPos(0, 0)
        # represent the statu of the chessboard, 0 standing for nothing, 1 standing for black
        # chessman, 2 standing for white
        # TODO:change the 2 dimensions chessboard into 1 dimension totally to lessen search time
        self.situation_matrix = [([0] * 15) for i in range(0, 15)]
        self.available = [0 for i in range(255)]

        # stack for black pie/ce and white chess
        self.black_chessman_queue = deque()
        self.white_chessman_queue = deque()

        # some argument for a play
        self.num_pieces = 0
        self.play_turn = []

        self.addItem(self.chessboard)

        # some uct arguments
        self.uct_root = Node()
        self.uct_current_root = self.uct_root
        self.uct_calculation_time = float(single_move_time)
        self.max_actions = max_actions
        self.confident = 1.96
        self.plays = {}
        self.wins = {}
        self.max_depth = 1
        pass

    def full(self):
        count = 0
        empty_pos = None
        for i in range(15):
            for j in range(15):
                if self.situation_matrix[i][j] != 0:
                    count += 1
                    empty_pos = (i, j)
                    if count >= 2:
                        return 2,(0,0)
        return count, empty_pos

    # Standard UCT functions

    def get_action(self):
        next_move_x = 0
        next_move_y = 0
        count, empty_pos = self.full()
        if count == 1:
            return empty_pos
        self.plays = {}
        self.wins = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.uct_calculation_time:
            board_copy = copy.deepcopy(self.situation_matrix)
            play_turn_copy = copy.deepcopy(self.num_pieces)
            self.run_simulation(board_copy, play_turn_copy)
            simulations += 1
        return next_move_x, next_move_y

    # TODO:Trans these codes into my framework

    def run_simulation(self, board, play_turn):
        """
        MCTS main process
        """

        plays = self.plays
        wins = self.wins
        availables = board.availables

        player = self.get_player(play_turn)  # 获取当前出手的玩家
        visited_states = set()  # 记录当前路径上的全部着法
        winner = -1
        expand = True

        # Simulation
        for t in range(1, self.max_actions + 1):
            # Selection
            # 如果所有着法都有统计信息，则获取UCB最大的着法
            if all(plays.get((player, move)) for move in availables):
                log_total = log(
                    sum(plays[(player, move)] for move in availables))
                value, move = max(
                    ((wins[(player, move)] / plays[(player, move)]) +
                     sqrt(self.confident * log_total / plays[(player, move)]), move)
                    for move in availables)
            else:
                # 否则随机选择一个着法
                move = choice(availables)

            board.update(player, move)

            # Expand
            # 每次模拟最多扩展一次，每次扩展只增加一个着法
            if expand and (player, move) not in plays:
                expand = False
                plays[(player, move)] = 0
                wins[(player, move)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, move))

            is_full = not len(availables)
            win, winner = self.has_a_winner(board)
            if is_full or win:  # 游戏结束，没有落子位置或有玩家获胜
                break

            player = self.get_player(play_turn)

        # Back-propagation
        for player, move in visited_states:
            if (player, move) not in plays:
                continue
            plays[(player, move)] += 1  # 当前路径上所有着法的模拟次数加1
            if player == winner:
                wins[(player, move)] += 1  # 获胜玩家的所有着法的胜利次数加1

    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p

    def select_one_move(self):
        percent_wins, move = max(
            (self.wins.get((self.player, move), 0) /
             self.plays.get((self.player, move), 1),
             move)
            for move in self.board.availables)  # 选择胜率最高的着法

        return move

    def has_a_winner(self, board):
        """
        检查是否有玩家获胜
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if (len(moved) < self.n_in_row + 2):
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = self.n_in_row
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

    def __str__(self):
        return "AI"




    # mouse press event
    def mousePressEvent(self, event):
        super(PSingleModel, self).mousePressEvent(event)
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

                    # AI's turn
                    self.num_pieces += 1
                    # uct search for best solution
                    next_move_row, next_move_col = self.uct_search(self.situation_matrix)

                    self.situation_matrix[next_move_row][next_move_col] = 2
                    temp_white_chessman = WhiteChessMan(self)
                    temp_white_chessman.set_index_pos(next_move_col, next_move_row)
                    temp_white_chessman.setPos(self.chessboard.left_up_x + next_move_col * self.chessboard.space - 17,
                                                self.chessboard.left_up_y + next_move_row * self.chessboard.space - 17)
                    print("while_chess_index_pos (%d, %d)" %(next_move_col, next_move_row))
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



class Node:
    def __init__(self):
        self.choice = (0, 0)
        self.visitedNum = 0
        self.fatherNode = None
        self.children = []
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
