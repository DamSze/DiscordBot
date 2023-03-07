import discord
import openai
import requests
import io
from discord.ext import commands
from const.constants import OPEN_AI_KEY
from const.constants import EMOJI


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = OPEN_AI_KEY
        self.error_emoji = EMOJI['actually']
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
        embed = discord.Embed(description="WAIT FOR YOUR IMAGES",
                              color=discord.Color.green())
        await ctx.send(embed=embed)
        images = openai.Image.create(
            prompt=prompt,
            n=4,
            size="256x256"
        )
        test = images['data']
        for img in test:
            file = self.downloadImage(img['url'])
            if not file:
                commands.CommandError("can't download image")
                return
            await ctx.channel.send(file=discord.File(file, 'image.png'))

    @gptimage.error
    async def gptimage_error(self, ctx, error):
        embed = discord.Embed(description=f'{self.error_emoji} {error} {self.error_emoji}',
                              color=discord.Color.red())
        await ctx.send(embed=embed)

    def downloadImage(self, url):
        img = requests.get(url)
        if img.status_code != 200:
            return False
        img_content = img.content
        return io.BytesIO(img_content)

async def setup(bot):
    await bot.add_cog(Gpt(bot))
