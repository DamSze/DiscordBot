import random
import discord
from discord.ext import commands
import bot


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, num: int, times:int):
        for i in range(0, times):
            await ctx.send(random.randint(0, num))





async def setup(bot):
    await bot.add_cog(Response(bot))
