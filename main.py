#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import *

from PController import PController

print('Hello')

if __name__ == '__main__':
    print('hello')
    app = QApplication(sys.argv)
    print('step1')
    mainController = PController()
    # print("i love u")
    sys.exit(app.exec_())

# a matrix for chess board
