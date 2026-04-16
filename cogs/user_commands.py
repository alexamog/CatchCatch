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
!help       — Show a summary of all commands.
"""

import random
import discord
from discord.ext import commands
from database import db


def _rarity_color(value: int) -> discord.Color:
    """Return a Discord embed colour matching the character's rarity tier.

    Args:
        value: The character's point value.

    Returns:
        A ``discord.Color`` corresponding to the rarity tier.
    """
    if value >= 2000:
        return discord.Color.gold()
    if value >= 500:
        return discord.Color.purple()
    if value >= 200:
        return discord.Color.blue()
    if value >= 50:
        return discord.Color.green()
    return discord.Color.greyple()


def _paginate(lines: list[str], max_len: int = 1900) -> list[str]:
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

    def __init__(self, bot: commands.Bot) -> None:
        """Initialise the cog with a reference to the bot instance.

        Args:
            bot: The running discord.ext.commands.Bot instance.
        """
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx: commands.Context[commands.Bot]) -> None:
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
    async def roll(self, ctx: commands.Context[commands.Bot]) -> None:
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

        embed = discord.Embed(title=picked['name'], color=_rarity_color(picked['value']))
        embed.add_field(name='Value', value=str(picked['value']), inline=True)
        embed.add_field(name='Owner', value=ctx.author.mention, inline=True)
        if picked['image_url']:
            embed.set_image(url=picked['image_url'])
        embed.set_footer(text=f'Rolled by {ctx.author.display_name}')
        await ctx.channel.send(embed=embed)

    @commands.command(name='discard')
    async def discard(self, ctx: commands.Context[commands.Bot], character_name: str) -> None:
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
    async def info(self, ctx: commands.Context[commands.Bot], character_name: str) -> None:
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

        status = f'<@{char["owner_id"]}>' if char['owned'] else 'Available'
        embed = discord.Embed(title=char['name'], color=_rarity_color(char['value']))
        embed.add_field(name='Value', value=str(char['value']), inline=True)
        embed.add_field(name='Owner', value=status, inline=True)
        if char['image_url']:
            embed.set_image(url=char['image_url'])
        await ctx.channel.send(embed=embed)

    @commands.command(name='collection')
    async def collection(self, ctx: commands.Context[commands.Bot]) -> None:
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
    async def available(self, ctx: commands.Context[commands.Bot]) -> None:
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

    @commands.command(name='help')
    async def help_command(self, ctx: commands.Context[commands.Bot]) -> None:
        """Show a summary of all available commands.

        Displays player commands and admin commands in a formatted embed.
        """
        embed = discord.Embed(
            title='CatchCatch Commands',
            color=discord.Color.blurple()
        )
        embed.add_field(
            name='Player Commands',
            value=(
                '`!register` — Register to play\n'
                '`!roll` — Roll for a random character\n'
                '`!discard [name]` — Return a character to the pool\n'
                '`!info [name]` — View character details\n'
                '`!collection` — View your collection and points\n'
                '`!available` — List all unclaimed characters\n'
                '`!help` — Show this message'
            ),
            inline=False
        )
        embed.add_field(
            name='Admin Commands',
            value='`!create [name] [value]` — Add a character to the pool *(requires Admin role)*',
            inline=False
        )
        embed.add_field(
            name='Rarity Tiers',
            value=(
                '⬜ Common — value 10\n'
                '🟩 Uncommon — value 50\n'
                '🟦 Rare — value 200\n'
                '🟪 Epic — value 500\n'
                '🟨 Legendary — value 2000'
            ),
            inline=False
        )
        await ctx.channel.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Register the UserFunctions cog with the bot."""
    await bot.add_cog(UserFunctions(bot))
