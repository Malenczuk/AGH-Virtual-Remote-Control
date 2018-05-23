from PyQt5.QtWidgets import *
from remotecontroller.room import Room
from remotecontroller.gui.item_widget import ItemWidget


class RoomWidget(QWidget):

    def __init__(self, room: Room, transmitter, parent=None):
        super(self.__class__, self).__init__(parent)
        self.room = room
        self.transmitter = transmitter
        self.vLayout = QVBoxLayout(self)
        self.__init_label()
        self.__init_items()

    def __init_label(self):
        self.label = QLabel(self.room.name, self)
        self.vLayout.addWidget(self.label)

    def __init_items(self):
        # initializing
        for item in self.room.items:
            item.widget = ItemWidget(item, self.transmitter, self)
            self.vLayout.addWidget(item.widget)

