from PyQt5.QtWidgets import *
import re
from remotecontroller.room import Room


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
            items = [item for item in room.items if re.search(query, item.description, re.IGNORECASE)]
            if items:
                self.itemsInRoom.append(Room(room.name, items))

    def __form_update(self):
        for i in reversed(range(self.formLayout.count())):
            widgetToRemove = self.formLayout.itemAt(i).widget()
            self.formLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        for room in self.itemsInRoom:
            roomLabel = QLabel(room.name, self)
            self.formLayout.addWidget(roomLabel)
            for item in room.items:
                button = QPushButton(item.description)
                button.clicked.connect(item.toggle_state)
                button.clicked.connect(self.__form_update)
                label = QLabel(" on  " if item.state else " off ")
                label.setStyleSheet("color: rgb(0, 255, 0);" if item.state else "color: rgb(255, 0, 0);")
                label.setFixedWidth(25)
                self.formLayout.addRow(label, button)

    def __layout(self):
        self.setMinimumSize(400, 400)
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
