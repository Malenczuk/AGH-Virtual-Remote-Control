from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from time import strftime
import re


class MainWindow(QMainWindow):

    def __init__(self, rooms, parent=None):
        super(MainWindow, self).__init__(parent)
        self.rooms = rooms
        self.initUI()

    def initUI(self):
        self.resize(300, 300)
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

class RoomsWidget(QWidget):

    def __init__(self, parent):
        super(RoomsWidget, self).__init__(parent)
        self.__mainWindow = parent
        self.shownRoom = []
        self.__controls()
        self.__layout()

    def __controls(self):
        self.roomsLable = QLabel("Room")
        self.roomsComboBox = QComboBox(self)
        self.roomsComboBox.addItems([""]+[room[0] for room in self.__mainWindow.rooms])
        self.roomsComboBox.currentTextChanged.connect(self.__combobox_update)
        self.roomsComboBox.currentTextChanged.connect(self.__form_update)
        self.mainMenuButton = QPushButton("Main Manu")
        self.mainMenuButton.clicked.connect(self.__main_menu_button_clicked)

    def __main_menu_button_clicked(self):
        self.__mainWindow.set_main_widget()

    def __combobox_update(self, value):
        self.shownRoom = [room for room in self.__mainWindow.rooms if room[0] == value]

    def __form_update(self):
        for i in reversed(range(self.formLayout.count())):
            widgetToRemove = self.formLayout.itemAt(i).widget()
            self.formLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        for room in self.shownRoom:
            for item in room[1]:
                button = QPushButton(item.description)
                button.clicked.connect(item.toggle_state)
                button.clicked.connect(self.__form_update)
                label = QLabel("on" if item.state else "off")
                self.formLayout.addRow(label, button)

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.h1box = QHBoxLayout()
        self.h2box = QHBoxLayout()

        self.searchResults = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.searchResults.addWidget(self.scrollArea)
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)

        self.h1box.addWidget(self.mainMenuButton)
        self.h2box.addWidget(self.roomsComboBox)

        self.vbox.addLayout(self.h1box)
        self.vbox.addLayout(self.h2box)
        self.vbox.addLayout(self.searchResults)
        self.__form_update()
        self.setLayout(self.vbox)

class SearchWidget(QWidget):

    def __init__(self, parent):
        super(SearchWidget, self).__init__(parent)
        self.__mainWindow = parent
        self.itemsInRoom = self.__mainWindow.rooms
        self.__controls()
        self.__layout()

    def __controls(self):
        self.searchLabel = QLabel("Search Items", self)
        self.searchQuery = QLineEdit(self)
        self.searchQuery.textEdited.connect(self.__search_query_edited)
        self.searchQuery.textEdited.connect(self.__form_update)
        self.mainMenuButton = QPushButton("Main Manu")
        self.mainMenuButton.clicked.connect(self.__main_menu_button_clicked)

    def __main_menu_button_clicked(self):
        self.__mainWindow.set_main_widget()

    def __search_query_edited(self):
        query = self.searchQuery.text()
        self.itemsInRoom = []
        for room in self.__mainWindow.rooms:
            items = [item for item in room[1] if re.search(query, item.description, re.IGNORECASE)]
            if items:
                self.itemsInRoom.append((room[0], items))

    def __form_update(self):
        for i in reversed(range(self.formLayout.count())):
            widgetToRemove = self.formLayout.itemAt(i).widget()
            self.formLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        for room in self.itemsInRoom:
            roomLabel = QLabel(room[0], self)
            self.formLayout.addWidget(roomLabel)
            for item in room[1]:
                button = QPushButton(item.description)
                button.clicked.connect(item.toggle_state)
                button.clicked.connect(self.__form_update)
                lable = QLabel("on" if item.state else "off")
                self.formLayout.addRow(lable, button)

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.h1box = QHBoxLayout()
        self.h2box = QHBoxLayout()

        self.searchResults = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.searchResults.addWidget(self.scrollArea)
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.h1box.addWidget(self.mainMenuButton)
        self.h2box.addWidget(self.searchLabel)
        self.h2box.addWidget(self.searchQuery)

        self.vbox.addLayout(self.h1box)
        self.vbox.addLayout(self.h2box)
        self.vbox.addLayout(self.searchResults)
        self.__form_update()
        self.setLayout(self.vbox)

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
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.searchButton)
        self.hbox.addWidget(self.roomsButton)

        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)


class RcWindow(QMainWindow):
    def __init__(self, rooms):
        super().__init__()
        self.rooms = rooms
        self.shownRooms = []
        self.initUI()

    def initUI(self):
        self.b_1 = QPushButton("Rooms")
        self.b_1.resize(100, 200)
        self.b_2 = QPushButton("Search")
        self.b_2.resize(100, 200)
        self.b_2.move(200, 0)
        self.mainwidget = QWidget(self)
        self.layout = QVBoxLayout(self.mainwidget)
        self.layout.addWidget(self.b_1)
        self.layout.addWidget(self.b_2)
        # self.scrollArea = QScrollArea(self.centralwidget)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.verticalLayout.addWidget(self.scrollArea)
        # self.setCentralWidget(self.centralwidget)
        # self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        #
        # self.cb_1 = QComboBox(self)
        # self.cb_1.addItems([room[0] for room in self.rooms])
        # self.cb_1.currentTextChanged.connect(self.on_combobox_changed)
        # self.cb_1.currentTextChanged.connect(self.update_after)
        # self.formLayout.addWidget(self.cb_1)

        self.resize(300, 300)
        self.setWindowTitle('Virtual Remote Controller')
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/resources/rc-icon.png'))
        self.center()
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_combobox_changed(self, value):
        self.shownRooms = [room for room in self.rooms if room[0] == value]
        print("elo")

    def update_after(self):
        for i in reversed(range(self.formLayout.count())):
            widgetToRemove = self.formLayout.itemAt(i).widget()
            self.formLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        self.formLayout.addWidget(self.cb_1)
        for room in self.shownRooms:
            for item in room[1]:
                button = QPushButton(item.description + "\t State: " + ("on" if item.state else "off"))
                button.clicked.connect(item.toggle_state)
                button.clicked.connect(self.update_after)
                self.formLayout.addWidget(button)