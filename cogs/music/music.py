import discord
from const.constants import EMOJI
from discord.ext import commands, tasks
from yt_dlp import YoutubeDL
from cogs.music.buttons import PlayButton, QueueButton


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_emoji = EMOJI["actually"]
        self.success_emoji = EMOJI["success"]
        self.running_emoji = EMOJI['running']
        self.infinity_emoji = EMOJI['infinity']
        self.play_emoji = EMOJI['play']
        self.is_playing = False
        self.is_paused = False
        self.skipped = False
        self.loop = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                title = info['title']
                yt_url = info['webpage_url']
                info = info['formats']
                mp4_url = [f for f in info if f.get('audio_ext') != 'none'][1]['url']
            except Exception as e:
                print(e)
                return False
        return {'source': mp4_url, 'title': title, 'url': yt_url}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            if self.loop is not True:
                self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                # task made to check whether there are any user on the channel
                self.empty_channel.start(ctx)
                if self.vc is None:
                    embed = discord.Embed(description=f"{self.error_emoji}CAN'T CONNECT TO THE VOICE CHANNEL{self.error_emoji}", colour=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            if not self.skipped and self.loop is not True:
                print(f"skipped value {self.skipped}")
                self.music_queue.pop(0)
                self.skipped = True
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next())

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            embed = discord.Embed(description=f"{self.error_emoji}CONNECT TO A VOICE CHANNEL{self.error_emoji}", colour=discord.Color.red())
            await ctx.send(embed=embed)
            return
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                embed = discord.Embed(description=f"{self.error_emoji}CAN'T FIND A SONG TRY DIFFERENT KEYWORD{self.error_emoji}", colour=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"{self.success_emoji} SONG ADDED TO THE QUEUE {self.success_emoji}", title=song['title'], url=song['url'], colour=discord.Color.green())
                await ctx.send(embed=embed, view = PlayButton(self, ctx))
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(aliases=['stop'])
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()

            embed = discord.Embed(description=f"PAUSED {self.play_emoji}", colour=discord.Color.purple())
            await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            embed = discord.Embed(description=f"RESUMED {self.play_emoji}", colour=discord.Color.purple())
            await ctx.send(embed=embed)

    @commands.command(aliases=['s'])
    async def skip(self, ctx, *args):
        if self.is_playing:
            self.vc.stop()
            self.skipped = True
            await self.play_music(ctx)

    @commands.command(aliases=['list'])
    async def queue(self, ctx, *args):
        try:
            if len(self.music_queue) > 0:
                queue = ''
                for i in range(0, len(self.music_queue)):
                    if i > 8:
                        queue += f'...[{len(self.music_queue)-8}]...'
                        break
                    queue += f"{str(i+1)}. {self.music_queue[i][0]['title']} {self.success_emoji}\n\n"
                embed = discord.Embed(title='QUEUE', description=queue, colour=discord.Color.green())
                await ctx.send(embed=embed, view=QueueButton(self, ctx))
            else:
                embed = discord.Embed(description=f"{self.error_emoji}QUEUE IS EMPTY{self.error_emoji}", colour=discord.Color.green())
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(aliases=['q_clr'])
    async def queue_clr(self, ctx, *args):
        if self.is_playing:
            self.vc.stop()
        self.music_queue = []
        embed = discord.Embed(description=f"{self.success_emoji}QUEUE CLEARED{self.success_emoji}",colour=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=['q', 'leave'])
    async def quit(self, ctx, *args):
        await self.quit_h()
    async def quit_h(self):
        if self.vc is not None:
            self.music_queue = []
            self.is_playing = False
            self.is_paused = False
            self.loop = False
            await self.vc.disconnect()
            self.vc = None
            self.empty_channel.stop()

    @commands.command(aliases=['lp'])
    async def loop(self, ctx, *args):
        if self.vc is None:
            return
        if self.loop is not True:
            self.loop = True
            embed = discord.Embed(description=f"LOOP ON {self.infinity_emoji}",colour=discord.Color.purple())
            await ctx.send(embed=embed)
        else:
            self.loop = False
            embed = discord.Embed(description=f"LOOP OFF {self.error_emoji}", colour=discord.Color.purple())
            await ctx.send(embed=embed)

    @tasks.loop(seconds=5)
    async def empty_channel(self, ctx):
        if self.vc is not None:
            try:
                if len(self.vc.channel.members) <= 1:
                    await self.quit_h()
                    self.empty_channel.stop()
                    embed = discord.Embed(description=f"{self.running_emoji}NO ONE LEFT IMMA HEAD OUT{self.running_emoji}", colour=discord.Color.blue())
                    await ctx.send(embed=embed)

            except Exception(IndexError) as e:
                print(e)



async def setup(bot):
    await bot.add_cog(Music(bot))


