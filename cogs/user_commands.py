import discord
import random
from discord.ext import commands
db = {}  # Temporary
users = []  # temprary


class UserFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx):
        """Provides the user the Gatcha role"""
        role = discord.utils.get(self.bot.get_guild(
            ctx.guild.id).roles, id=909238338509217805)
        if role in ctx.author.roles:  # Checks if the user already has the specified role
            return await ctx.channel.send(f'You already have the {role} role.')
        await ctx.author.add_roles(role)
        await ctx.channel.send(f'You now have the {role} role!')
        return users.append(ctx.author)

    @commands.command(name='roll')
    @commands.has_role('Gatcha')
    async def roll_dice(self, ctx):
        """This function gives a chance for the user to recieve a character."""
        roll_done = False
        list_of_pp = []
        for characters in db.keys():
            if db[characters].owned == False:
                list_of_pp.append(characters)

        if len(list_of_pp) == 0:
            return await ctx.channel.send(f'It seems all characters have been claimed D:')

        while roll_done == False:
            random_character = random.choice(list_of_pp)
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
        for player in users:
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


def setup(bot):
    bot.add_cog(UserFunctions(bot))
