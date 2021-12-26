import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.command()
async def load(ctx, extension):  # This loads all the extensions
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):  # This unpacks/unloads the extensions
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # We take out the last 3 characters (.py) since we already specify files that end with .py
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)