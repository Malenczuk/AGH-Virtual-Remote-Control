from remotecontroller.room import Room
from remotecontroller.gui.item_widget import ItemWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re



class MainWidget(QWidget):

    def __init__(self, parent):
        super(MainWidget, self).__init__()
        self.parent = parent
        self.shownRoom = self.parent.rc.rooms
        self.itemsInRooms = self.parent.rc.rooms
        self.__controls()
        self.__layout()
        self.form_update()

    def __controls(self):
        self.roomsLabel = QLabel("Room")
        self.roomsLabel.setFixedWidth(35)
        self.roomsComboBox = QComboBox(self)
        self.roomsComboBox.addItems(["ALL"] + [room.name for room in self.parent.rc.rooms])
        self.roomsComboBox.currentTextChanged.connect(self.__combobox_update)
        self.searchLabel = QLabel("Search Items", self)
        self.searchQuery = QLineEdit(self)
        self.searchQuery.textEdited.connect(self.__search_query_edited)

    def __combobox_update(self, value):
        self.shownRoom = [room for room in self.parent.rc.rooms if room.name == value or value == "ALL"]
        self.__search_query_edited()

    def __search_query_edited(self):
        query = self.searchQuery.text()
        self.itemsInRooms = []
        for room in self.shownRoom:
            items = [item for item in room.items if re.search(query, item.description, re.IGNORECASE)]
            if items:
                self.itemsInRooms.append(Room(room.name, items))
        self.form_update()

    def form_update(self):
        for i in reversed(range(self.VScrollLayout.count())):
            widget = self.VScrollLayout.itemAt(i).widget()
            show = False
            for room in self.itemsInRooms:
                if isinstance(widget, QLabel):
                    if widget.text() == room.name:
                        show = True
                if isinstance(widget, ItemWidget):
                    for item in room.items:
                        if widget.item == item:
                            show = True
            if show:
                widget.show()
            else:
                widget.hide()

    def __layout(self):
        self.setMinimumSize(400, 400)
        self.vMainBox = QVBoxLayout()
        self.hRoomBox = QHBoxLayout()
        self.hSearchBox = QHBoxLayout()

        self.__init_vertical_scroll_layout()

        self.__init_item_widgets()

        self.hRoomBox.addWidget(self.roomsLabel)
        self.hRoomBox.addWidget(self.roomsComboBox)
        self.hSearchBox.addWidget(self.searchLabel)
        self.hSearchBox.addWidget(self.searchQuery)

        self.vMainBox.addLayout(self.hRoomBox)
        self.vMainBox.addLayout(self.hSearchBox)
        self.vMainBox.addLayout(self.searchResults)

        self.setLayout(self.vMainBox)

    def __init_vertical_scroll_layout(self):
        self.searchResults = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.searchResults.addWidget(self.scroll_area)
        self.VScrollLayout = QVBoxLayout(self.scroll_area_widget_contents)
        self.VScrollLayout.setAlignment(Qt.AlignTop)

    def __init_item_widgets(self):
        for room in self.itemsInRooms:
            room_label = QLabel(room.name, self)
            self.VScrollLayout.addWidget(room_label)
            for item in room.items:
                item_widget = ItemWidget(item, self.parent.rc.transmitter, self)
                self.VScrollLayout.addWidget(item_widget)
