import locale


class Room:

    def __init__(self, name, items, parent=None):
        self.name = name
        self.items = items
        self.parent = parent
        self.widget = None

    def __lt__(self, other):
        # making object possible to sort using user locale
        return locale.strxfrm(self.name) < locale.strxfrm(other.name)
