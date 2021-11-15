import json
from models import Character
from discord.ext import commands


class AdminFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = []
        self.characters = {'characters': []}
        with open('database/user_db.json') as fp:
            data = json.load(fp)
            for user in data:
                self.users.append(user)
        with open('database/character_db.json') as fp:
            data = json.load(fp)
            for character in data['characters']:
                self.characters['characters'].append(
                    {
                        'character_name': character['character_name'],
                        'character_value': character['character_value'],
                        'owned': character['owned'],
                        'owner_id': character['owner_id']
                    })

    @commands.command(name='create')
    # @commands.has_role('Admin')
    async def create(self, ctx, name, value):
        """Creates a character. Usage: !create [Character name] [Value] """
        new_char = Character(name, value)
        self.characters['characters'].append({ #CHANGE THIS LATER
            "character_name": new_char.name,
            "character_value": new_char.value,
            "owned": new_char.owned,
            "owner_id": ctx.author.id
        })
        self.write_to_char_db()
        await ctx.channel.send(f'Character name: {name} value: {value}')

    def write_to_user_db(self):
        with open('database/user_db.json', 'w') as fp:
            json.dump(self.users, fp)

    def write_to_char_db(self):
        with open('database/character_db.json', 'w') as fp:
            json.dump(self.characters, fp)


def setup(bot):
    bot.add_cog(AdminFunctions(bot))
