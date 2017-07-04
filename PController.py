import sys

from PModel import *
from PStartMenuView import *
from PyQt5.QtWidgets import *


class PController(QMainWindow):
    def __init__(self):
        super(PController, self).__init__()
        self.MainView = QGraphicsView()
        self.current_model = None
        self.setGeometry(500,200,700,700)
        self.setWindowTitle("Gobang")
        self.setCentralWidget(self.MainView)

        self.load_start_menu()

        pass

    def load_start_menu(self):
        self.current_model = PStartMenu()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    def load_single_model(self):
        self.current_model = PSingleModel()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    def load_multiple_model(self):
        self.current_model = PMultipleModel()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)


    @pyqtSlot(int, name = "ChangeModel")
    def ChangeModel(self, model_code):
        if model_code == 1:
            self.load_single_model()
            print("get signal 1")
        pass
        if model_code == 2:
            self.load_multiple_model()
            print("get signal 2")
        pass
        if model_code == 3:
            self.load_start_menu()
            print("get signal 3")
        pass

