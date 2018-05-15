from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQuick import *

from remotecontroller.gui.mainWidget import MainWidget
from remotecontroller.gui.roomsWidget import RoomsWidget
from remotecontroller.gui.searchWidget import SearchWidget


class MainWindow(QMainWindow):

    def __init__(self, rooms, parent=None):
        super(MainWindow, self).__init__(parent)
        self.rooms = rooms
        self.initUI()

    def initUI(self):
        self.resize(400, 400)
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

    def set_search_widget(self):
        self.search_widget = SearchWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.search_widget)
        self.setCentralWidget(_widget)

    def set_rooms_widget(self):
        self.rooms_widget = RoomsWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.rooms_widget)
        self.setCentralWidget(_widget)
