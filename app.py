"""
app.py
------
Entry point for the CatchCatch Discord bot.

Loads all cogs from the cogs/ directory automatically on startup, then
starts the bot using the token stored in the DISCORD_TOKEN environment
variable (read from .env).
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    """Load a cog by name. Bot owner only.

    Usage: !load [cog name]
    """
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unload a cog by name. Bot owner only.

    Usage: !unload [cog name]
    """
    bot.unload_extension(f'cogs.{extension}')


@bot.command(name='slap')
async def slap(ctx, target: discord.Member):
    """EASTER EGG — Slap another server member.

    Usage: !slap [@user]

    Args:
        target: The Discord member to slap.
    """
    await ctx.channel.send(f'{ctx.author.mention} slapped {target.mention}!')


bot.run(TOKEN)
