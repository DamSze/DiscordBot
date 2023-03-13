import random
import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from const.constants import EMOJI
from discord.ext.commands import parameter as param

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_emoji = EMOJI['actually']

    @commands.command(aliases=['rol', 'dice'], brief='roll custom dice', help='returns random number in range.\n\n'
                                                                            'Usage: !roll [num] [times] [True/False]\n')
    async def roll(self, ctx, num: int = param(description="(mandatory): roll range (0,num)"),
                   times: int = param(default=1, description='(optional): number of rolls'),
                   oneline: bool = param(default=False, description='(optional): if True writes result in one line')):
        if times <= 0 or num <= 0:
            raise commands.BadArgument('ARGUMENT CANNOT BE <=0')
            return

        elif num > 1000000:
            raise commands.BadArgument('MAX ROLL CAN BE UP TO 1 MILLION')
            return

        elif times > 100:
            raise commands.BadArgument('MAX NUMBER OF ROLLS CAN BE UP TO 100')
            return

        res = []
        mess = ''
        for i in range(0, times):
            rand_val = random.randint(0, num)
            res.append(rand_val+1)
        if oneline:
            embed = discord.Embed(title='Roll 🎲', description=res, color=discord.Color.purple())
        else:
            for num in res:
                mess = mess + str(num) + '\n'
            embed = discord.Embed(title='Roll 🎲', description=mess, color=discord.Color.purple())
        await ctx.send(embed=embed)

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(description=f'{self.error_emoji} {error} {self.error_emoji}',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=['random_color', 'rgb'], brief='random color', help='return random color in viusal, hex and rgb form\n\n'
                                                                            'Usage: !color\n')
    async def color(self, ctx):
        hex = discord.Color.random()
        rgb = hex.to_rgb()
        embed = discord.Embed(color=hex)
        embed.add_field(name='Hex', value=str(hex))
        embed.add_field(name='RGB', value=str(rgb)[1:-1])
        await ctx.send(embed=embed)

    @commands.command(aliases=['film'], brief='random movie', help='returns one of 250 IMBD best rated movies\n\n'
                                                                            'Usage: !movie\n')
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
