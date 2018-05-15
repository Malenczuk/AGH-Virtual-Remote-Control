from PyQt5.QtWidgets import *


class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.__mainWindow = parent
        self.__controls()
        self.__layout()

    def __controls(self):
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.__search_button_clicked)
        self.roomsButton = QPushButton("Rooms")
        self.roomsButton.clicked.connect(self.__rooms_button_clicked)

    def __search_button_clicked(self):
        self.__mainWindow.set_search_widget()

    def __rooms_button_clicked(self):
        self.__mainWindow.set_rooms_widget()

    def __layout(self):
        self.setMinimumSize(400, 400)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.searchButton)
        self.hbox.addWidget(self.roomsButton)

        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)