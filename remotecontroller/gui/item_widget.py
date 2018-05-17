from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os


class ItemWidget(QWidget):

    def __init__(self, item, transmitter, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.parent = parent
        self.item = item
        self.transmitter = transmitter
        self.v_layout = QHBoxLayout()
        self.setLayout(self.v_layout)
        self.__init_item_state_label()
        self.__init_item_button()

    def __init_item_button(self):
        self.button = QPushButton(self)
        self.button.setText(self.item.description)
        self.button.clicked.connect(self.__clicked_action)
        self.v_layout.addWidget(self.button)

    def __clicked_action(self):
        self.transmitter(self.item)
        self.item.toggle_state()
        if self.item.state:
            self.label.setPixmap(self.on_pixmap)
        else:
            self.label.setPixmap(self.off_pixmap)

    def __init_item_state_label(self):
        self.label = QLabel("on" if self.item.state else "off")
        self.label.setToolTip("on" if self.item.state else "off")
        self.label.setStyleSheet("color: rgb(0, 255, 0);" if self.item.state else "color: rgb(255, 0, 0);")
        self.off_pixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-off-icon32.png')
        self.on_pixmap = QPixmap(os.path.dirname(__file__) + '/resources/switch-on-icon32.png')
        self.label.setPixmap(self.off_pixmap)
        self.label.setFixedWidth(32)
        self.v_layout.addWidget(self.label)
