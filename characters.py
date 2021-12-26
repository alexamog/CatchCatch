class Character:
    def __init__(self, name, value, owned=False, owner=None):
        self.name = name
        self.value = int(value)
        self.owned = owned
        self._owner = owner

    def owned(self):
        return self.owned

    def discard(self):
        self._owner = None
        self.owned = False

    @property
    def owner(self):
        """Returns the value of the owner"""
        return self._owner