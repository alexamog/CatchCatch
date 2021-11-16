import json
import discord
import random
from discord.ext import commands


class UserFunctions(commands.Cog):
    def __init__(self, bot):
        """Loads all the databases and initializes the discord bot"""
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

    @commands.command(name='register')
    async def register(self, ctx):
        """Provides the user the Gatcha role"""

        # Checks if the user already has the specified role and is inside the user db
        if ctx.author.id in self.users:
            return await ctx.channel.send(f'You are already in the db.')

        self.users.append(ctx.author.id)
        await ctx.channel.send(f'You have been added to the db')
        return self.__save_user_db()

    @commands.command(name='roll')
    @commands.has_role('Gatcha')
    async def roll_dice(self, ctx):
        """This function gives a chance for the user to recieve a character."""
        available_characters = []
        for characters in self.characters['characters']:
            if characters['owned'] == False:
                available_characters.append(characters)
        if len(available_characters) == 0:
            return await ctx.channel.send(f'It seems all characters have been claimed D:')

        random_character = random.choice(available_characters)
        self.__add_character(ctx.author.id, random_character)
        await ctx.channel.send(f'{ctx.author.mention}, you got {random_character["character_name"]} with a value of {random_character["character_value"]}!')
        return self.__save_character_db()

    @commands.command(name='discard')
    @commands.has_role('Gatcha')
    async def trade(self, ctx, character_name):
        """Lets the user trade with another user."""
        if self.__discard_character(ctx.author.id, character_name):
            return await ctx.channel.send(f'Character successfully discarded')
        await ctx.channel.send(f'{ctx.author.mention}, it seems you do not own that character.')

    @commands.command(name='info')
    async def info(self, ctx, character_name):
        """Usage: !info [Character name]"""
        result = self.get_character_info(character_name)
        await ctx.channel.send(f'{result}')
    @commands.command(name='collection')
    async def info(self, ctx):
        """Lets the user see their character collection"""
        characters_owned = self.get_player_characters(ctx.author.id)
        characters_owned = ' '.join(characters_owned)
        characters_owned = characters_owned.replace(' ','\n')
        await ctx.channel.send(f'{characters_owned}')

    def __save_user_db(self):
        with open('database/user_db.json', 'w') as fp:
            json.dump(self.users, fp)

    def __add_character(self, user_id, selected_character):
        """Changes the character's attributes to make them be own by the user"""
        for picked_char in self.characters['characters']:
            if picked_char['character_name'] == selected_character['character_name']:
                picked_char['owned'] = True
                picked_char['owner_id'] = user_id
                self.__save_character_db()

    def __discard_character(self, user_id, character_name):
        """Lets the user discard the character"""
        for character in self.characters['characters']:
            if character['character_name'] == character_name and character['owner_id'] == user_id:
                character['owned'] = False
                character['owner_id'] = "None"
                self.__save_character_db()
                return True
        return False

    def __save_character_db(self):
        with open('database/character_db.json', 'w') as fp:
            json.dump(self.characters, fp)

    def get_character_info(self, character_name):
        for current_character in self.characters['characters']:
            if current_character['character_name'] == character_name:
                if current_character['owned'] == True:
                    return f'```Character name: {current_character["character_name"]}\nCharacter Value: {current_character["character_value"]}\nOwned: {current_character["owned"]}```'
                return f'```Character name: {current_character["character_name"]}\nCharacter Value: {current_character["character_value"]}\nOwned: {current_character["owned"]}```'
    def get_player_characters(self,owner_id):
        list_of_char = []
        for current_character in self.characters['characters']:
            if current_character['owner_id'] == owner_id:
                list_of_char.append(current_character['character_name'])
        return list_of_char
def setup(bot):
    bot.add_cog(UserFunctions(bot))
