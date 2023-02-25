import discord
from discord.ext import commands

class PlayButton(discord.ui.View):
    def __init__(self, music, ctx):
        super().__init__()
        self.music = music
        self.ctx = ctx
    @discord.ui.button(label='skip', style=discord.ButtonStyle.green)
    async def skipButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('skipped')
        await self.music.skip(self.ctx)

    @discord.ui.button(emoji='⏸', style=discord.ButtonStyle.green)
    async def pauseButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('paused')
        await self.music.pause(self.ctx)

    @discord.ui.button(emoji='⏯', style=discord.ButtonStyle.green)
    async def resumeButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('resumed')
        await self.music.resume(self.ctx)

    @discord.ui.button(emoji='📜', style=discord.ButtonStyle.green)
    async def queueButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('queue')
        await self.music.queue(self.ctx)