import random
import discord
import requests
from discord.ext import commands


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

    @commands.command(aliases=['random_color', 'rgb'])
    async def color(self, ctx):
        hex = discord.Color.random()
        rgb = hex.to_rgb()
        embed = discord.Embed(color=hex)
        embed.add_field(name='Hex', value=str(hex))
        embed.add_field(name='RGB', value=str(rgb)[1:-1])
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Other(bot))
