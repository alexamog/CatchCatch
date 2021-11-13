import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

from models import Character

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

bot = commands.Bot(command_prefix='!')

db = {}


@bot.command(name='roll')
async def roll_dice(ctx):
    roll_done = False
    tries = 0
    while roll_done == False and tries < len(db.keys()): #While the user has not received a charactr who is not owned or the code has not runs out of characters,
        random_character = random.choice(list(db.keys()))
        tries += 1
        if db[random_character].owned == False:
            db[random_character].owner = ctx.author
            await ctx.channel.send(f'{ctx.author.mention}, you got {random_character}!')
            roll_done = True
            return
        else:
            tries += 1
    await ctx.channel.send(f'It seems all characters have been claimed D:')


@bot.command(name='create')
@commands.has_role('Admin')
async def create(ctx, name, value):
    db[name] = Character(name, value)
    await ctx.channel.send(f'Character name: {name} value: {value}')


@bot.command(name='info')
async def create(ctx, character_name):
    if character_name not in db.keys():
        await ctx.channel.send(f'Character: {character_name} not in database.')
    await ctx.channel.send(db[character_name])


@bot.command(name='trade')
async def trade(ctx, target: discord.Member):
    pass


@bot.command(name='slap')
async def trade(ctx, target: discord.Member):
    await ctx.channel.send(f'{ctx.author.mention} slapped {target.mention}!')

bot.run(TOKEN)
