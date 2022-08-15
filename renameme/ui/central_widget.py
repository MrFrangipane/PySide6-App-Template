from PySide6.QtWidgets import QWidget, QGridLayout


class CentralWidget(QWidget):
    def __init__(self, app, parent=None):
        QWidget.__init__(self, parent)

        self._app = app
