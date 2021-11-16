import json
from models import Character
from discord.ext import commands


class AdminFunctions(commands.Cog):
    def __init__(self, bot):
        """Loads all the characters and initializes the discord bot instance"""
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
        if name.isalpha() == False or value.isnumeric() == False:
            return await ctx.channel.send(f'Invalid input.')
        self.__add_character(new_char)
        await ctx.channel.send(f'Character name: {name} value: {value}')

    def __add_character(self, character):
        """Adds a character into the database"""
        self.characters['characters'].append({
            "character_name": character.name,
            "character_value": character.value,
            "owned": character.owned,
            "owner_id": "None"
        })
        self.__save_character_db()

    def __save_character_db(self):
        """Saves the character db"""
        with open('database/character_db.json', 'w') as fp:
            json.dump(self.characters, fp)


def setup(bot):
    bot.add_cog(AdminFunctions(bot))
