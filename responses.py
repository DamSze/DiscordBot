import random
import asyncio
import discord
from discord.ext import commands
import bot


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, num: int, times: int = 1, oneline: bool = False):
        res = []
        for i in range(0, times):
            rand_val = random.randint(0, num)
            res.append(rand_val)
        if oneline:
            await ctx.send(res)
        else:
            for num in res:
                await ctx.send(num)

    @roll.error
    async def missing_argument(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Not enough arguments given")





async def setup(bot):
    await bot.add_cog(Response(bot))
