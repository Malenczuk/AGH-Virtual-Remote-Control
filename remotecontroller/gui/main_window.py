from remotecontroller.gui.main_widget import MainWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import os


class MainWindow(QMainWindow):

    def __init__(self, rc, parent=None):
        super(self.__class__, self).__init__(parent)
        self.rc = rc
        self.mainWidget = MainWidget(self)
        self.__init_ui()

    def __init_ui(self):
        self.resize(500, 600)
        self.setWindowTitle('Virtual Remote Controller')
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/resources/rc-icon.png'))
        # centering main window
        self.center()
        # setting main widget
        self.setCentralWidget(self.mainWidget)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
