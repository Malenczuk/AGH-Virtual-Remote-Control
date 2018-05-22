import locale


class Item:

    def __init__(self, id, description, state=False, parent=None):
        self.id = id
        self.description = description
        self.state = state
        self.parent = parent
        self.widget = None

    def __lt__(self, other):
        return locale.strxfrm(self.description) < locale.strxfrm(other.description)

    def toggle_state(self, state="toggle"):
        self.state = True if state == "on" else (False if state == "off" else not self.state)
        if self.widget:
            self.widget.toggle()
