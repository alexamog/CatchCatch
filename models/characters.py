import discord

class Character:
    def __init__(self, name, value, owners = [], times_owned = []):
        self.name = name
        self.value = int(value)
        self._owners = owners #list of owners
        self.times_owned = times_owned #list of natural to times owned for each owner

    @property
    def owners(self):
        """Returns the value of the owners"""
        return self._owners

    def owned(self):
        discord.User.id in self._owners

    def discard(self):
        uid = discord.User.id
        ownlist = self._owners
        owntimes = self.times_owned
        if uid not in ownlist:
            print('You do not own this character.')
        else:
             self._owners = ownlist.remove(ownlist[ownlist.index(uid)])
             self.times_owned = owntimes.remove(owntimes[owntimes.index(uid)])