from remotecontroller.gui.main_widget import MainWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import os


class MainWindow(QMainWindow):

    def __init__(self, rc, parent=None):
        super(MainWindow, self).__init__(parent)
        self.rc = rc
        self.initUI()

    def initUI(self):
        self.resize(500, 600)
        self.setWindowTitle('Virtual Remote Controller')
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/resources/rc-icon.png'))
        self.center()
        self.set_main_widget()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_main_widget(self):
        self.main_widget = MainWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.main_widget)
        self.setCentralWidget(_widget)

