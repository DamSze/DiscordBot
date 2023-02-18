import random
import asyncio
import discord
from discord.ext import commands
import bot


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rol', 'dice'])
    async def roll(self, ctx, num: int, times: int = 1, oneline: bool = False):
        res = []
        mess=''
        for i in range(0, times):
            rand_val = random.randint(0, num)
            res.append(rand_val)
        if oneline:
            embed = discord.Embed(title='Roll 🎲', description=res, color=discord.Color.purple())
            await ctx.send(embed=embed)
        else:
            for num in res:
                mess = mess + str(num) + '\n'
            embed = discord.Embed(title='Roll 🎲', description=mess, color=discord.Color.purple())
            await ctx.send(embed=embed)

    @roll.error
    async def missing_argument(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Not enough arguments given")





async def setup(bot):
    await bot.add_cog(Other(bot))
