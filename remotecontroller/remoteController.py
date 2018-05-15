# -*- coding: utf-8 -*-
import sys
from remotecontroller.gui.mainWindow import *
from remotecontroller.item import Item
from remotecontroller.qdarkstyle import load_stylesheet_pyqt5
import yaml


class RemoteController:

    def __init__(self, file):
        data = []
        with open(file, 'r') as stream:
            try:
                data = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.rooms = [(room[0][0], [Item(id, description) for id, description in room[1:]]) for room in
                      map(lambda x: list(x.items()), data)]

    def gui(self):
        app = QApplication(sys.argv)
        dark_stylesheet = load_stylesheet_pyqt5()
        app.setStyleSheet(dark_stylesheet)
        win = MainWindow(self.rooms)

        app.exec_()


def main():
    RemoteController(os.path.dirname(__file__) + "/resources/configuration.yml").gui()


if __name__ == "__main__":
    main()
