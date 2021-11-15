import json
import discord
import random
from discord.ext import commands

from models import characters


class UserFunctions(commands.Cog):
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

    @commands.command(name='register')
    async def register(self, ctx):
        """Provides the user the Gatcha role"""
        role_id = 909351178888953896  # Change this depending on server role
        role = discord.utils.get(self.bot.get_guild(
            ctx.guild.id).roles, id=role_id)

        # Checks if the user already has the specified role and is inside the user db
        if ctx.author.id in self.users:
            return await ctx.channel.send(f'You are already in the db.')

        self.users.append(ctx.author.id)
        await ctx.author.add_roles(role)
        await ctx.channel.send(f'You have been added to the db and now have the {role} role!')
        return self.write_to_user_db()

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
        for picked_char in self.characters['characters']:
            if picked_char['character_name'] == random_character['character_name']:
                print('FOUND')
                picked_char['owned'] = True
                picked_char['owner_id'] = ctx.author.id
                self.write_to_char_db()
        print(self.characters)
        return await ctx.channel.send(f'{ctx.author.mention}, you got {random_character}!')

    @commands.command(name='discard')
    @commands.has_role('Gatcha')
    async def trade(self, ctx, character_name):
        """Lets the user trade with another user."""
        if self.characters[character_name].owner == ctx.author:
            self.characters[character_name].discard()
            return await ctx.channel.send(f'{ctx.author.mention}, you have discarded {character_name} successfully.')
        await ctx.channel.send(f'{ctx.author.mention}, it seems you do not own that character.')

    @commands.command(name='scoreboard')
    async def scoreboard(self, ctx):
        """Displays all users who are enrolled followed by their points."""
        for player in self.users:
            points = 0
            for characters in self.characters.keys():
                if self.characters[characters].owner == player:
                    points += self.characters[characters].value
            await ctx.channel.send(f'Player: {player} Points: {points}')

    @commands.command(name='info')
    async def info(self, ctx, character_name):
        """Usage: !info [Character name]"""
        if character_name not in self.characters.keys():
            await ctx.channel.send(f'Character: {character_name} not in database.')
        await ctx.channel.send(f'```Name: {self.characters[character_name].name}\nValue: {self.characters[character_name].value}\nOwned: {self.characters[character_name].owned} ```')
        if discord.File(f'photo_db/{character_name.lower()}.jpg'):
            await ctx.channel.send(file=discord.File(f'photo_db/{character_name.lower()}.jpg'))

    def write_to_user_db(self):
        with open('database/user_db.json', 'w') as fp:
            json.dump(self.users, fp)

    def write_to_char_db(self):
        with open('database/character_db.json', 'w') as fp:
            json.dump(self.characters, fp)


def setup(bot):
    bot.add_cog(UserFunctions(bot))
