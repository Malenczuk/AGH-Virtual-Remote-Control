import sys

sys.path.append("../Malenczuk_Marcin")
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
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
        # changing style of the application
        self.app.setStyleSheet(qdarksyle.load_stylesheet_pyqt5())
        # creating main window of the application
        self.win = MainWindow(self)
        # creating second thread of continuous receiving messages from server
        self.receiver = self.Receiver(self.UDPSock)
        # signaling main thread of received message
        self.receiver.update.connect(self.toggle)
        # starting receiving thread
        self.receiver.start()

    def toggle(self, msg):
        # changing state of an item in received message
        msgs = msg.split()
        for room in self.rooms:
            for item in room.items:
                if len(msgs) == 2 and item.id == msgs[1]:
                    item.toggle_state(msgs[0])

    def gui(self):
        self.app.exec_()

    def transmitter(self, item):
        # sending message to server
        MESSAGE = ("off " if item.state else "on ") + item.id
        self.UDPSock.sendto(MESSAGE.encode('utf8'), (RemoteController.SERVER_UDP_IP, RemoteController.SERVER_UDP_PORT))

    class Receiver(QThread):
        # creating signal
        update = pyqtSignal(str)

        def __init__(self, UDPSock, parent=None):
            super(self.__class__, self).__init__(parent)
            self.UDPSock = UDPSock

        def run(self):
            while True:
                data, addr = self.UDPSock.recvfrom(2018)
                if not data:
                    break
                self.update.emit(data.decode())


def parse_yaml(file):
    """
    :param file: yaml file with configuration of rooms
    :return: parsed list of rooms with items within
    """
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
