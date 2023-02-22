import discord
from discord.ext import commands
from discord.utils import find
from cogs import other, cat, moderate, pokemon


class Bot:
    def __init__(self):
        self.token = "MTA1MDAyOTQyODQ2MzM3ODQ5Mw.GGQQkr.DR8qlfCrhCJkADH8lUknccJAv9RY18eVkWONy8"
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True, description='askdhgaskudhgiuahsdgijsadhgjkahs')

    def run_discord_bot(self):
        @self.bot.event
        async def on_guild_join(guild):
            general = find(lambda x: x.name == 'general', guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                embed = discord.Embed(title='Hello!', description='Bot made by Mordzio type\n!help to see commands', color=discord.Color.green())
                await general.send(embed=embed)

        @self.bot.event
        async def on_ready():
            await update_status()
            await setup()
            print(f"{self.bot.user} is now running!")

        @self.bot.event
        async def on_member_join(member):
            await update_status()
            channel_id = 1074133871962099732
            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(title='New member joined', description=f'{member} has now officially become a loser', color=discord.Color.blue())
            await channel.send(embed=embed)

        @self.bot.event
        async def on_member_remove(member):
            await update_status()
            channel_id = 1074133871962099732
            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(title='User left',description=f"{member} has regained it's connection the outer world", color=discord.Colour.red())
            await channel.send(embed=embed)
            print('member removed')

        @self.bot.event
        async def on_command_error(ctx, error):
            print(error)
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(description='❌PERMISSION DENIED❌', color=discord.Color.red())
                await ctx.send(embed=embed)
            elif isinstance(error, commands.MemberNotFound):
                embed = discord.Embed(description='❌USER NOT FOUND❌', color=discord.Color.red())
                await ctx.send(embed=embed)

        async def update_status():
            members_count = (self.bot.guilds[0].member_count - 1)
            status = str(members_count) + (' users' if members_count > 1 else ' user')
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

        async def setup():
            await other.setup(self.bot)
            await cat.setup(self.bot)
            await moderate.setup(self.bot)
            await pokemon.setup(self.bot)


        self.bot.run(self.token)


