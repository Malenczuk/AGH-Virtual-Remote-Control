# -*- coding: utf-8 -*-
from socket import *


class Receiver:

    def __init__(self):
        self.UDP_IP = "255.255.255.255"
        self.UDP_PORT = 2018
        # Create socket and bind to address
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)
        self.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.UDPSock.bind((self.UDP_IP, self.UDP_PORT))
        # Receive messages
        while True:
            data, addr = self.UDPSock.recvfrom(2018)
            if not data:
                break
            print(data.decode('utf8'), addr)

        # Close socket
        self.UDPSock.close()


def main():
    Receiver()


if __name__ == '__main__':
    main()
