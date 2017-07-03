#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import *

from PController import PController

print('Hello')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainController = PController()
    mainController.show()
    sys.exit(app.exec_())

# a matrix for chess board
