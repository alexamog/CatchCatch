class Character:
    def __init__(self, name, value, owned=False):
        self.name = name
        self.value = value
        self.owned = owned

    def __owned__(self):
        return self.owned
