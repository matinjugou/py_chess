from PModel import *


class PController(QObject):
    def __init__(self, current_mode: PModel = None, parent: QObject = None):
        super(PController, self).__init__(parent)
        self.MainView = QGraphicsView()
        self.current_model = current_mode
        self.MainView.show()

        #only for test, to delete later
        new_game = PMultipleModel()
        self.load_model(new_game)

        pass

    def load_model(self, new_model):
        self.MainView.setScene(new_model)
        pass