import discord
import openai
import requests
import io
from discord.ext import commands
from const.constants import OPEN_AI_KEY


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = OPEN_AI_KEY
        openai.api_key = self.key

    @commands.command()
    async def gpt(self, ctx, *args):
        prompt = " ".join(args)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0,
        )
        embed = discord.Embed(description=response['choices'][0]['text'].strip(), color = discord.Color.green())
        print(response)
        await ctx.send(embed=embed)

    @commands.command(aliases=['image', 'Aiimage', 'imageAi', 'picture'])
    async def gptimage(self, ctx, *args):
        prompt = " ".join(args)
        images = openai.Image.create(
            prompt=prompt,
            n=4,
            size="256x256"
        )
        test = images['data']
        for img in test:
            file = self.downloadImage(img['url'])
            await ctx.channel.send(file=discord.File(file, 'image.png'))

    def downloadImage(self, url):
        img = requests.get(url)
        img_content = img.content
        return io.BytesIO(img_content)

async def setup(bot):
    await bot.add_cog(Gpt(bot))
