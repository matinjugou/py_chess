#!/usr/bin/python3
from PController import *

print('Hello')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainController = PController()
    mainController.show()
    sys.exit(app.exec_())

# a matrix for chess board
