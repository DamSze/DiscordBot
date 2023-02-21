import random
import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup


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

    @commands.command(aliases=['film'])
    async def movie(self, ctx):
        response = requests.get('https://www.imdb.com/chart/top/')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        movie_tags = soup.select('td.titleColumn')
        rand_movie = random.randint(1, 250)

        movie_info = filter(lambda x: x != ',', movie_tags[rand_movie].text.split())
        for link in soup.select('td.posterColumn')[rand_movie].select('img'):
            movie_img = link.get('src')
        movie_thumbnail = movie_img

        movie_info = list(movie_info)
        # deleting number on IMBD website
        movie_info.pop(0)
        # removing brackets
        title = movie_info[0:-1]
        release_year = movie_info[-1]
        title = ' '.join(str(x) for x in title)
        release_year = release_year[1:-1]

        embed = discord.Embed(color=discord.Color.purple())
        embed.add_field(name='Title:', value=title)
        embed.add_field(name='Released:', value=release_year, inline=False)
        embed.set_thumbnail(url=movie_thumbnail)
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Other(bot))
