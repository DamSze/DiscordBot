import requests
import discord
import json
from discord.ext import commands


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = 'live_tv19fCPO2u6LBPa4vYReChLicROoIPfLV2yZOBb7QQvyYM9QPa8KtECgdklZPN58'

    @commands.command(aliases=['psycha', 'kot'])
    async def cat(self, ctx, limit: int = 1):
        if limit > 10:
            limit = 10
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=' + str(limit) + '&api_key=' + self.key)
        if response.status_code != 200:
            await ctx.send("API error, could not get a cat")
        for i in range(0, limit):
            pic = response.json()[i]['url']
            await ctx.send(pic)




async def setup(bot):
    await bot.add_cog(Cat(bot))