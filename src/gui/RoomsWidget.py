from PyQt5.QtWidgets import *


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
        self.setMinimumSize(400,400)
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
