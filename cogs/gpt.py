import discord
import openai
from discord.ext import commands
from const.constants import OPEN_AI_KEY


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = OPEN_AI_KEY

    @commands.command()
    async def gpt(self, ctx, *args):
        try:
            prompt = " ".join(args)
            openai.api_key = self.key
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.5,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=["You:"]
            )
            embed = discord.Embed(description=response['choices'][0]['text'], color = discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Gpt(bot))
