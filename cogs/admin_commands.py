"""
cogs/admin_commands.py
----------------------
Admin-only commands for CatchCatch.

All commands in this cog require the invoking user to have the 'Admin'
role in the Discord server. Unauthorised attempts are caught by the error
handler and returned as a friendly message.

Commands
--------
!create — Add a new character to the gacha pool.
"""

from discord.ext import commands
from database import db


class AdminFunctions(commands.Cog):
    """Cog containing admin-only bot commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialise the cog with a reference to the bot instance.

        Args:
            bot: The running discord.ext.commands.Bot instance.
        """
        self.bot = bot

    @commands.command(name='create')
    @commands.has_role('Admin')
    async def create(self, ctx: commands.Context[commands.Bot], name: str, value: str, image_url: str | None = None) -> None:
        """Add a new character to the gacha pool.

        Usage: !create [name] [value] [image_url]

        The name must contain only letters and the value must be a
        positive integer. Duplicate names are rejected. The image URL
        is optional — if provided it is shown in roll and info embeds.
        Requires the 'Admin' role.

        Args:
            name: Display name for the new character (letters only).
            value: Point value for the new character (positive integer).
            image_url: Optional direct image URL to display in embeds.
        """
        if not name.isalpha():
            return await ctx.channel.send('Character name must contain only letters.')
        if not value.isnumeric():
            return await ctx.channel.send('Character value must be a positive number.')
        if db.character_exists(name):
            return await ctx.channel.send(f'A character named **{name}** already exists.')

        db.create_character(name, int(value), image_url)
        msg = f'Created character **{name}** with value **{value}**.'
        if image_url:
            msg += f' Image set.'
        await ctx.channel.send(msg)

    @create.error
    async def create_error(self, ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
        """Handle errors raised by the !create command.

        Catches missing-role errors and replies with a clear message.
        All other errors are re-raised for the global error handler.

        Args:
            error: The exception raised during command execution.
        """
        if isinstance(error, commands.MissingRole):
            await ctx.channel.send('You need the Admin role to use this command.')
        else:
            raise error


async def setup(bot: commands.Bot) -> None:
    """Register the AdminFunctions cog with the bot."""
    await bot.add_cog(AdminFunctions(bot))
