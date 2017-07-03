from PModel import *
from PyQt5.QtWidgets import *
import sys


class PController(QMainWindow):
    def __init__(self):
        super(PController, self).__init__()
        self.MainView = QGraphicsView()
        self.current_model = None
        self.setGeometry(700,700,700,700)
        self.setWindowTitle("Gobang")
        self.setCentralWidget(self.MainView)

        # only for test, to delete later
        new_game = PMultipleModel()
        self.load_model(new_game)

        pass

    def load_model(self, new_model):
        self.MainView.setScene(new_model)
        pass

    def load_single_model(self):
        self.current_model = PSingleModel()
        self.current_model.exitcurrentmodel.connect(self.ChangeModel)
        self.MainView.setScene(self.current_model)

    @pyqtSlot(int, name="ChangeModel")
    def ChangeModel(self, model_code):
        if model_code == 1:
            self.load_single_model()
        pass