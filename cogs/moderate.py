import discord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def clr(self, ctx, num: int = 1):
        await ctx.channel.purge(limit=num + 1)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title='KICK', description=f'Kicked {member}', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title='BAN', description=f'Banned {member}', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = [entry async for entry in ctx.guild.bans(limit=2000)]
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title='UNBAN', description=f'unbanned {user.name}#{user.discriminator}', color=discord.Color.green())
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mod(bot))
