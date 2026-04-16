"""
app.py
------
Entry point for the CatchCatch Discord bot.

Initialises the SQLite database, loads all cogs from the cogs/ directory
automatically on startup, then starts the bot using the token stored in
the DISCORD_TOKEN environment variable (read from .env).
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise RuntimeError('DISCORD_TOKEN is not set in .env')

db.init_db()
db.seed_characters()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def setup_hook() -> None:
    """Load all cogs from the cogs/ directory on startup."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context[commands.Bot], extension: str) -> None:
    """Load a cog by name. Bot owner only.

    Usage: !load [cog name]
    """
    await bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context[commands.Bot], extension: str) -> None:
    """Unload a cog by name. Bot owner only.

    Usage: !unload [cog name]
    """
    await bot.unload_extension(f'cogs.{extension}')


@bot.command(name='slap')
async def slap(ctx: commands.Context[commands.Bot], target: discord.Member) -> None:
    """EASTER EGG — Slap another server member.

    Usage: !slap [@user]

    Args:
        target: The Discord member to slap.
    """
    await ctx.channel.send(f'{ctx.author.mention} slapped {target.mention}!')


bot.run(TOKEN)
