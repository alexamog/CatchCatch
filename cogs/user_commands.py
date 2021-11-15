import json
import discord
import random
from discord.ext import commands
db = {}  # Temporary


class UserFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {'users': []}
        with open('database/user_db.json') as fp:
            data = json.load(fp)
            for user in data['users']:
                self.users['users'].append(
                    {'user_ID': user['user_ID'], 'characters_owned': user['characters_owned']})

    @commands.command(name='register')
    async def register(self, ctx):
        """Provides the user the Gatcha role"""
        role_id = 909351178888953896  # Change this depending on server role
        role = discord.utils.get(self.bot.get_guild(
            ctx.guild.id).roles, id=role_id)

        # Checks if the user already has the specified role and is inside the user db
        for players in self.users['users']:
            if ctx.author.id == players['user_ID']:
                return await ctx.channel.send(f'You are already in the db.')

        self.users['users'].append(
            {"user_ID": ctx.author.id, "characters_owned": []})
        await ctx.author.add_roles(role)
        await ctx.channel.send(f'You have been added to the db and now have the {role} role!')
        return self.write_to_user_db()

    @commands.command(name='roll')
    @commands.has_role('Gatcha')
    async def roll_dice(self, ctx):
        """This function gives a chance for the user to recieve a character."""
        roll_done = False
        available_characters = []
        for characters in db.keys():
            if db[characters].owned == False:
                available_characters.append(characters)

        if len(available_characters) == 0:
            return await ctx.channel.send(f'It seems all characters have been claimed D:')

        while roll_done == False:
            random_character = random.choice(available_characters)
            if db[random_character].owned == False:
                db[random_character].owner = ctx.author
                await ctx.channel.send(f'{ctx.author.mention}, you got {random_character}!')
                roll_done = True

    @commands.command(name='discard')
    @commands.has_role('Gatcha')
    async def trade(self, ctx, character_name):
        """Lets the user trade with another user."""
        if db[character_name].owner == ctx.author:
            db[character_name].discard()
            return await ctx.channel.send(f'{ctx.author.mention}, you have discarded {character_name} successfully.')
        await ctx.channel.send(f'{ctx.author.mention}, it seems you do not own that character.')

    @commands.command(name='scoreboard')
    async def scoreboard(self, ctx):
        """Displays all users who are enrolled followed by their points."""
        for player in self.users:
            points = 0
            for characters in db.keys():
                if db[characters].owner == player:
                    points += db[characters].value
            await ctx.channel.send(f'Player: {player} Points: {points}')

    @commands.command(name='info')
    async def info(self, ctx, character_name):
        """Usage: !info [Character name]"""
        if character_name not in db.keys():
            await ctx.channel.send(f'Character: {character_name} not in database.')
        await ctx.channel.send(f'```Name: {db[character_name].name}\nValue: {db[character_name].value}\nOwned: {db[character_name].owned} ```')
        if discord.File(f'photo_db/{character_name.lower()}.jpg'):
            await ctx.channel.send(file=discord.File(f'photo_db/{character_name.lower()}.jpg'))

    def write_to_user_db(self):
        with open('database/user_db.json', 'w') as fp:
            json.dump(self.users, fp)


def setup(bot):
    bot.add_cog(UserFunctions(bot))
