"""
cogs/user_commands.py
---------------------
Player-facing commands for CatchCatch.

Commands
--------
!register   — Register to play.
!roll       — Roll for a random available character.
!discard    — Return an owned character to the pool.
!info       — Look up details on any character.
!collection — View your own character collection and total points.
!available  — List all characters not yet claimed.
"""

import random
from discord.ext import commands
from database import db


def _paginate(lines: list, max_len: int = 1900) -> list:
    """Split a list of text lines into Discord-safe message chunks.

    Discord enforces a 2000-character message limit. This helper groups
    lines into pages that stay under *max_len* characters so each chunk
    can be sent as a separate message without hitting that limit.

    Args:
        lines: Individual lines of text to paginate.
        max_len: Maximum character length per page. Defaults to 1900 to
            leave headroom for code-block formatting.

    Returns:
        A list of strings, each safe to send as a single Discord message.
    """
    pages, current, length = [], [], 0
    for line in lines:
        if length + len(line) + 1 > max_len:
            pages.append('\n'.join(current))
            current, length = [], 0
        current.append(line)
        length += len(line) + 1
    if current:
        pages.append('\n'.join(current))
    return pages


class UserFunctions(commands.Cog):
    """Cog containing all player-facing bot commands."""

    def __init__(self, bot):
        """Initialise the cog with a reference to the bot instance.

        Args:
            bot: The running discord.ext.commands.Bot instance.
        """
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx):
        """Register your Discord account to play CatchCatch.

        Adds your user ID to the player database so you can use !roll
        and other commands. Safe to call multiple times — duplicate
        registrations are ignored with a friendly message.
        """
        if db.is_registered(ctx.author.id):
            return await ctx.channel.send('You are already registered.')
        db.register_user(ctx.author.id)
        await ctx.channel.send('You have been registered!')

    @commands.command(name='roll')
    async def roll(self, ctx):
        """Roll for a random available character.

        Picks a random unowned character from the pool and assigns it to
        you. Requires prior registration via !register. If no characters
        remain in the pool, a message is displayed instead.
        """
        if not db.is_registered(ctx.author.id):
            return await ctx.channel.send('You need to register first with `!register`.')

        available = db.get_available_characters()
        if not available:
            return await ctx.channel.send('All characters have been claimed!')

        picked = random.choice(available)
        db.claim_character(picked['name'], ctx.author.id)
        await ctx.channel.send(
            f'{ctx.author.mention} rolled **{picked["name"]}** (value: {picked["value"]})!'
        )

    @commands.command(name='discard')
    async def discard(self, ctx, character_name: str):
        """Return one of your characters to the unclaimed pool.

        Usage: !discard [character name]

        Args:
            character_name: Exact name of the character to discard.
        """
        if db.discard_character(character_name, ctx.author.id):
            await ctx.channel.send(f'**{character_name}** has been returned to the pool.')
        else:
            await ctx.channel.send(f'You do not own a character named **{character_name}**.')

    @commands.command(name='info')
    async def info(self, ctx, character_name: str):
        """Show details for any character regardless of ownership.

        Usage: !info [character name]

        Displays the character's name, point value, and current ownership
        status (available or owned by a specific player).

        Args:
            character_name: Exact name of the character to look up.
        """
        char = db.get_character(character_name)
        if not char:
            return await ctx.channel.send(f'No character named **{character_name}** found.')
        status = f'Owned by <@{char["owner_id"]}>' if char['owned'] else 'Available'
        await ctx.channel.send(
            f'```\nName:   {char["name"]}\nValue:  {char["value"]}\nStatus: {status}\n```'
        )

    @commands.command(name='collection')
    async def collection(self, ctx):
        """Display your character collection and total points.

        Lists every character you currently own along with its point value,
        then shows your cumulative score. Output is paginated automatically
        if your collection would exceed Discord's message length limit.
        """
        owned = db.get_player_characters(ctx.author.id)
        if not owned:
            return await ctx.channel.send(
                f'{ctx.author.mention}, you have no characters yet. Try `!roll`!'
            )
        lines = [f'Name: {c["name"]}, Value: {c["value"]}' for c in owned]
        total = sum(c['value'] for c in owned)
        for page in _paginate(lines):
            await ctx.channel.send(f'```\n{page}\n```')
        await ctx.channel.send(f'{ctx.author.mention}, total points: **{total}**')

    @commands.command(name='available')
    async def available(self, ctx):
        """List all characters that have not yet been claimed.

        Output is paginated automatically if the list would exceed
        Discord's message length limit.
        """
        avail = db.get_available_characters()
        if not avail:
            return await ctx.channel.send('All characters have been claimed!')
        lines = [f'Name: {c["name"]}, Value: {c["value"]}' for c in avail]
        for page in _paginate(lines):
            await ctx.channel.send(f'```\n{page}\n```')


def setup(bot):
    """Register the UserFunctions cog with the bot."""
    bot.add_cog(UserFunctions(bot))
