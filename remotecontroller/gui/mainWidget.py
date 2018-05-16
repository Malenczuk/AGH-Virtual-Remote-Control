from remotecontroller.room import Room
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import re
import os


class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.__mainWindow = parent
        self.shownRoom = self.__mainWindow.rooms
        self.itemsInRooms = self.__mainWindow.rooms
        self.__controls()
        self.__layout()
        self.__form_update()

    def __controls(self):
        self.roomsLabel = QLabel("Room")
        self.roomsLabel.setFixedWidth(35)
        self.roomsComboBox = QComboBox(self)
        self.roomsComboBox.addItems(["ALL"] + [room.name for room in self.__mainWindow.rooms])
        self.roomsComboBox.currentTextChanged.connect(self.__combobox_update)
        self.searchLabel = QLabel("Search Items", self)
        self.searchQuery = QLineEdit(self)
        self.searchQuery.textEdited.connect(self.__search_query_edited)

    def __combobox_update(self, value):
        self.shownRoom = [room for room in self.__mainWindow.rooms if room.name == value or value == "ALL"]
        self.__search_query_edited()

    def __search_query_edited(self):
        query = self.searchQuery.text()
        self.itemsInRooms = []
        for room in self.shownRoom:
            items = [item for item in room.items if re.search(query, item.description, re.IGNORECASE)]
            if items:
                self.itemsInRooms.append(Room(room.name, items))
        self.__form_update()

    def __form_update(self):
        for i in reversed(range(self.formLayout.count())):
            widget_to_remove = self.formLayout.itemAt(i).widget()
            self.formLayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        for room in self.itemsInRooms:
            room_label = QLabel(room.name, self)
            self.formLayout.addWidget(room_label)
            for item in room.items:
                button = self.__create_item_button(item)
                label = self.__create_item_state_label(item)

                self.formLayout.addRow(label, button)

    def __create_item_button(self, item):
        button = QPushButton(item.description)
        button.clicked.connect(item.toggle_state)
        button.clicked.connect(self.__form_update)
        return button

    def __create_item_state_label(self, item):
        label = QLabel("on" if item.state else "off")
        label.setToolTip("on" if item.state else "off")
        label.setStyleSheet("color: rgb(0, 255, 0);" if item.state else "color: rgb(255, 0, 0);")
        h = label.height()
        if item.state:
            pixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-on-icon32.png')
        else:
            pixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-off-icon32.png')
        label.setPixmap(pixmap)

        return label

    def __layout(self):
        self.setMinimumSize(400, 400)
        self.vMainBox = QVBoxLayout()
        self.hRoomBox = QHBoxLayout()
        self.hSearchBox = QHBoxLayout()

        self.searchResults = QVBoxLayout()
        self.formLayout = self.__create_form_layout(self.searchResults)

        self.hRoomBox.addWidget(self.roomsLabel)
        self.hRoomBox.addWidget(self.roomsComboBox)
        self.hSearchBox.addWidget(self.searchLabel)
        self.hSearchBox.addWidget(self.searchQuery)

        self.vMainBox.addLayout(self.hRoomBox)
        self.vMainBox.addLayout(self.hSearchBox)
        self.vMainBox.addLayout(self.searchResults)

        self.setLayout(self.vMainBox)

    def __create_form_layout(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget_contents = QWidget(scroll_area)
        scroll_area.setWidget(scroll_area_widget_contents)
        widget.addWidget(scroll_area)
        return QFormLayout(scroll_area_widget_contents)

