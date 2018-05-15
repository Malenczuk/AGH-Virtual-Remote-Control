# -*- coding: utf-8 -*-
import sys
import yaml
from remotecontroller.gui.MainWindow import *
from remotecontroller.Item import Item


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
        win = MainWindow(self.rooms)
        app.exec_()


def main():
    rc = RemoteController("resources/configuration.yml")
    rc.gui()


if __name__ == "__main__":
    main()
