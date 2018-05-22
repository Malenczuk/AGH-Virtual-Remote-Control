from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from remotecontroller.item import Item
import os


class ItemWidget(QWidget):

    def __init__(self, item: Item, transmitter, parent=None):
        super(self.__class__, self).__init__(parent)
        self.item = item
        self.transmitter = transmitter
        self.hLayout = QHBoxLayout(self)
        self.setLayout(self.hLayout)
        self.__init_item_state_label()
        self.__init_item_button()

    def __init_item_button(self):
        self.button = QPushButton(self)
        self.button.setText(self.item.description)
        self.button.clicked.connect(self.__clicked_action)
        self.hLayout.addWidget(self.button)

    def __clicked_action(self):
        self.transmitter(self.item)

    def toggle(self):
        self.label.setToolTip("on" if self.item.state else "off")
        self.label.setStyleSheet("color: rgb(0, 255, 0);" if self.item.state else "color: rgb(255, 0, 0);")
        if self.item.state:
            self.label.setPixmap(self.onPixmap)
        else:
            self.label.setPixmap(self.offPixmap)

    def __init_item_state_label(self):
        self.label = QLabel("on" if self.item.state else "off", self)
        self.label.setStyleSheet("color: rgb(0, 255, 0);" if self.item.state else "color: rgb(255, 0, 0);")
        self.offPixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-off-icon32.png')
        self.onPixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-on-icon32.png')
        if self.item.state:
            self.label.setPixmap(self.onPixmap)
        else:
            self.label.setPixmap(self.offPixmap)
        self.label.setFixedWidth(32)
        self.hLayout.addWidget(self.label)
