from PModel import *
from PyQt5.QtWidgets import *


class PController(QMainWindow):
    def __init__(self):
        super(PController, self).__init__()
        self.MainView = QGraphicsView()
        self.setFixedSize(700, 672)
        self.current_model = None
        self.setWindowTitle("Gobang")
        self.setCentralWidget(self.MainView)
        self.MainView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MainView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.load_start_menu()

        pass

    def load_start_menu(self):
        self.setFixedSize(700, 672)
        self.current_model = PStartMenu()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    def load_single_model(self):
        self.setFixedSize(700, 533)
        self.current_model = PSingleModel()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    def load_multiple_model(self):
        self.setFixedSize(700, 533)
        self.current_model = PMultipleModel()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    # load online model
    # TO DO
    def load_online_model(self):
        self.setFixedSize(700, 533)
        self.current_model = POnlineModel()
        self.current_model.Signal_ChangeModel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)
        pass

    @pyqtSlot(int, name = "ChangeModel")
    def ChangeModel(self, model_code):
        if model_code == 1:
            self.load_start_menu()
            print("get signal 1")
        pass
        if model_code == 2:
            self.load_multiple_model()
            print("get signal 2")
        pass
        if model_code == 3:
            self.load_single_model()
            print("get signal 3")
        pass
        if model_code == 4:
            self.load_online_model()
            print("get signal 4")
        pass

