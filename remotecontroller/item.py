from socket import *
import locale


class Item:
    UDP_IP = "255.255.255.255"
    UDP_PORT = 2018

    def __init__(self, id, description, state=False):
        self.id = id
        self.description = description
        self.state = state

    def __lt__(self, other):
        return locale.strxfrm(self.description) < locale.strxfrm(other.description)

    def toggle_state(self):
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        MESSAGE = ("off " if self.state else "on ") + self.id
        UDPSock.sendto(MESSAGE.encode('utf8'), (Item.UDP_IP, Item.UDP_PORT))
        UDPSock.close()
        self.state = not self.state