# -*- coding: utf-8 -*-
from socket import *
import yaml


class Item:
    UDP_IP = "255.255.255.255"
    UDP_PORT = 2018

    def __init__(self, id, description, state=False):
        self.id = id
        self.description = description
        self.state = state

    def toggle_state(self):
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        MESSAGE = ("off " if self.state else "on ") + self.id
        UDPSock.sendto(MESSAGE.encode('utf8'), (Item.UDP_IP, Item.UDP_PORT))
        UDPSock.close()
        self.state = not self.state


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


rc = RemoteController("configuration.yml")
rc.rooms[0][1][0].toggle_state()