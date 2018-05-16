import locale


class Room:

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def __lt__(self, other):
        return locale.strxfrm(self.name) < locale.strxfrm(other.name)
