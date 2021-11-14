from models import Character
from discord.ext import commands


class AdminFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create')
    # @commands.has_role('Admin')
    async def create(ctx, name, value):
        """Creates a character. Usage: !create [Character name] [Value] """
        # db[name] = Character(name, value)
        await ctx.channel.send(f'Character name: {name} value: {value}')


def setup(bot):
    bot.add_cog(AdminFunctions(bot))
