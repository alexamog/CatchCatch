import os
import discord
import random
from discord import errors
from discord.ext.commands.errors import MemberNotFound
from dotenv import load_dotenv
from discord.ext import commands

from models.characters import Character

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

db = {}


@bot.command(name='roll')
async def roll_dice(ctx):
    dice_roll = random.randint(0, 100)
    await ctx.channel.send(f'{ctx.author}, you rolled a {dice_roll}')


@bot.command(name='create')
@commands.has_role('Admin')
async def create(ctx, name, value):
    db[name] = Character(name, value)
    await ctx.channel.send(f'Character name: {name} Character value: {value}')


@bot.command(name='trade')
async def trade(ctx, target: discord.Member):
    await ctx.channel.send(f'{ctx.author.mention} slapped {target.mention}!')


@bot.command(name='get')
async def get(ctx):
    for character, worth in db.items():
        await ctx.channel.send(f'{character}, {worth}')


bot.run(TOKEN)
