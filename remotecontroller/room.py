import locale


class Room:

    def __init__(self, name, items, parent=None):
        self.name = name
        self.items = items
        self.parent = parent

    def __lt__(self, other):
        return locale.strxfrm(self.name) < locale.strxfrm(other.name)
