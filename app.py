import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

from models import Character
import requests
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='!')

db = {}
users = []


@bot.command(name='roll')
@commands.has_role('Gatcha')
async def roll_dice(ctx):
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


@bot.command(name='create')
@commands.has_role('Them')
async def create(ctx, name, value):
    db[name] = Character(name, value)
    await ctx.channel.send(f'Character name: {name} value: {value}')


@bot.command(name='info')
async def info(ctx, character_name):
    if character_name not in db.keys():
        await ctx.channel.send(f'Character: {character_name} not in database.')
    await ctx.channel.send(db[character_name])
    if discord.File(f'photo_db/{character_name.lower()}.jpg'):
        await ctx.channel.send(file=discord.File(f'photo_db/{character_name.lower()}.jpg'))


@bot.command(name='register')
async def info(ctx):
    role = discord.utils.get(bot.get_guild(
        ctx.guild.id).roles, id=909238338509217805)
    await ctx.author.add_roles(role)
    await ctx.channel.send(f'You now have the {role} role!')
    return users.append(ctx.author)


@bot.command(name='discard')
@commands.has_role('Gatcha')
async def trade(ctx, character_name):
    if db[character_name].owner == ctx.author:
        db[character_name].discard()
        return await ctx.channel.send(f'{ctx.author.mention}, you have discarded {character_name} successfully.')
    await ctx.channel.send(f'{ctx.author.mention}, it seems you do not own that character.')


@bot.command(name='leaderboards')
async def scoreboard(ctx):
    for player in users:
        points = 0
        for characters in db.keys():
            if db[characters].owner == player:
                points += db[characters].value
        await ctx.channel.send(f'Player: {player} Points: {points}')


@bot.command(name='slap')
async def trade(ctx, target: discord.Member):
    await ctx.channel.send(f'{ctx.author.mention} slapped {target.mention}!')


bot.run(TOKEN)
