class Character:
    def __init__(self, name, value, owned=False, owner=None):
        self.name = name
        self.value = int(value)
        self.owned = owned
        self._owner = owner

    def owned(self):
        return self.owned

    # def __str__(self):
    #     if self._owner == None:
    #         return f'```Character name: {self.name}\nValue: {self.value}```'
    #     return f'```Character name: {self.name}\nValue: {self.value}\nOwned by: {self._owner}\n```'

    def discard(self):
        self._owner = None
        self.owned = False

    @property
    def owner(self):
        """Returns the value of the owner"""
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner value"""
        if self.owned == False and self._owner == None:
            self._owner = owner
            self.owned = True
