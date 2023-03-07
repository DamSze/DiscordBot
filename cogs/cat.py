import requests
import discord
from const.constants import CAT_KEY, EMOJI
from discord.ext import commands


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = CAT_KEY
        self.error_emoji = EMOJI['actually']

    @commands.command(aliases=['psycha', 'kot'])
    async def cat(self, ctx, limit: int = 1):
        if limit > 10:
            limit = 10
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=' + str(limit)
                                + '&api_key=' + self.key)
        if response.status_code != 200:
            embed = discord.Embed(description=f"{self.error_emoji}Can't connect to the API{self.error_emoji}",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        for i in range(0, limit):
            pic = response.json()[i]['url']
            embed = discord.Embed(color=discord.Color.purple())
            embed.set_image(url=pic)
            await ctx.send(embed=embed)




async def setup(bot):
    await bot.add_cog(Cat(bot))