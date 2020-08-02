import asyncio
import discord
import youtube_dl
from gtts import gTTS
from discord.ext import commands
from functools import partial

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

queue = []
#Made global 8/2/20 use on youtest

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)


class Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))


    #https://cloud.google.com/speech-to-text/docs/languages
    @commands.command()
    async def speechVC(self, ctx, *, name):
        """Puts text to speech in the VC channel. Use as .speechVC {TTS}"""
        tts = gTTS(f'{name}', lang="en-IE")
        tts.save(f'speech.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('speech.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Playing tts in VC')

    @commands.command(description = "plays a youtube video. use .yt Followed by Link")
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

        @commands.command(description="plays a youtube video. use .yt Followed by Link")
        async def youtest(self, ctx, *, url):
            """Plays from a url (almost anything youtube_dl supports)"""



            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send('Now playing: {}'.format(player.title))


    @commands.command()
    async def ytTest(self, ctx, *, search: str):
        """In testing phase of Queueing songs"""
        player = self.get_player(ctx)

        async with ctx.typing():
            #source = await YTDLSource.from_url(url, loop=self.bot.loop)
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

            await player.queue.put(source)

        await ctx.send('Now playing: {}'.format(source.title))

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = Music(ctx)
            self.players[ctx.guild.id] = player

        return player


    @commands.command(description = "Streams. use  for larger videos./n .stream link")
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command(description = "Changes the player volume. CAN GO VERY LOUD. max is 100")
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(description = "Pauses the YT video")
    async def pause(self, ctx):
        """Pauses the YT link"""
        if ctx.voice_client.is_playing():
            await ctx.voice_client.pause()

    @commands.command(description = "Use after Pause")
    async def resume(self, ctx):
        """Resumes playing the music."""
        if not ctx.voice_client.is_playing():
            await ctx.voice_client.resume()


    @commands.command(description = "Disconnects from the voice channel")
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @speechVC.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(client):
    client.add_cog(Music(client))