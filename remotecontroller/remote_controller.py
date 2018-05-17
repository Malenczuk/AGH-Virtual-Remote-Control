import sys
sys.path.append("../AGH-Virtual-Remote-Control/")
from PyQt5.QtWidgets import QApplication
import remotecontroller.gui.qdarkstyle as qdarksyle
from remotecontroller.gui.main_window import MainWindow
from remotecontroller.room import Room
from remotecontroller.item import Item
from socket import *
import yaml
import os

class RemoteController:
    SERVER_UDP_IP = "255.255.255.255"
    SERVER_UDP_PORT = 2018

    def __init__(self, rooms):
        self.rooms = rooms
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)
        self.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(qdarksyle.load_stylesheet_pyqt5())
        self.win = MainWindow(self)

    def gui(self):
        self.app.exec_()

    def transmitter(self, item):
        MESSAGE = ("off " if item.state else "on ") + item.id
        self.UDPSock.sendto(MESSAGE.encode('utf8'), (RemoteController.SERVER_UDP_IP, RemoteController.SERVER_UDP_PORT))


def parse_yaml(file):
    data = []
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return sorted([Room(room[0][0], sorted([Item(id, description) for id, description in room[1:]]))
                   for room in map(lambda x: list(x.items()), data)])


def main():
    rooms = parse_yaml(os.path.dirname(__file__) + "/resources/configuration.yml")
    rc = RemoteController(rooms)
    rc.gui()


if __name__ == '__main__':
    main()