import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import youtube_dl


class VoiceChannelCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def joinVC(self, ctx):
        """Joins Voice Channel"""
        if ctx.author.voice.channel != None:
            await ctx.author.voice.channel.connect()
           # url = 'https://www.youtube.com/watch?v=rPOUewuNKFE'
            await ctx.send('I joined your channel.')
         #   player = await ctx.author.voice.channel.create_ytdl_player(url)
          #  player.start()
        else:
            await ctx.send('You are not in a voice channel!')


    @commands.command()
    async def jvcTest(self, ctx, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()




    @commands.command()
    async def leaveVC(self, ctx):
        """Leaves Voice Channel"""
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        await ctx.send('Left your voice channel')
        #for VoiceClient in commands.voice_clients:
        #    if VoiceClient.guild == ctx.guild:
         #       await VoiceClient.disconnect()
         #       await ctx.send('I left your voice channel.')


def setup(client):
    client.add_cog(VoiceChannelCog(client))
