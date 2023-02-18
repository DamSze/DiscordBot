import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import bot


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clr(self, ctx, num: int = 1):
        await ctx.channel.purge(limit=num + 1)

    @clr.error
    async def clr_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='❌ ERROR NO PERMISSION TO DELETE MESSAGES ❌', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='❌NO PERMISSION TO KICK MEMBERS ❌', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='❌USER NOT FOUND❌', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='❌NO PERMISSION TO BAN MEMBERS ❌', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='❌USER NOT FOUND❌', color=discord.Color.red())
            await ctx.send(embed=embed)




async def setup(bot):
    await bot.add_cog(Mod(bot))
