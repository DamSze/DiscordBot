import os
import discord
from discord.ext import commands
import responses
import cat


class Bot:
    def __init__(self):
        self.token = "MTA1MDAyOTQyODQ2MzM3ODQ5Mw.GGQQkr.DR8qlfCrhCJkADH8lUknccJAv9RY18eVkWONy8"
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

    def run_discord_bot(self):

        @self.bot.event
        async def on_ready():
            await setup()
            print(f"{self.bot.user} is now running!")

        @self.bot.event
        async def on_member_join(member):
            channel_id = 1074133871962099732
            channel = self.bot.get_channel(channel_id)
            await channel.send(f'{member} has now officially become a loser')

        @self.bot.event
        async def on_member_remove(member):
            channel_id = 1074133871962099732
            channel = self.bot.get_channel(channel_id)
            await channel.send(f"{member} has regained it's connection the outer world")

        async def setup():
            await responses.setup(self.bot)
            await cat.setup(self.bot)

        self.bot.run(self.token)


