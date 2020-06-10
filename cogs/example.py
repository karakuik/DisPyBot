import discord
from discord.ext import commands
import random
from gtts import gTTS
from copypasta import copypasta
import asyncio
import os


class Example(commands.Cog):

    def __init__(self, commands):
        self.commands = commands

    # if i want to create an event within a Cog
    # I need to have this decorator
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is online, from cog with love')

    # Commands
    @commands.command()
    async def ling(self, ctx):
        await ctx.send('Long from cog!')
        # Checks ping

    @commands.command()
    async def ping(self, ctx):
        """Checks the latency and if receiving commands"""
        await ctx.send(f'Pong! My Latency is {round(self.commands.latency * 1000)}ms')

    # Sends FizzBuzz
    @commands.command()
    async def fizz(self, ctx):
        await ctx.send('buzz!')

    # Clears the chat
    @commands.command()
    async def clear(self, ctx, amount=0):
        """Clears the chat. Use this followed by a #"""
        await ctx.channel.purge(limit=amount)
        if amount < 1:
            await ctx.send('Please state an amount. i.e. ".clear 5"')

    # Anyone wanna play league?
    @commands.command()
    async def league(self, ctx):
        """use this to check for homos in your area"""
        responses = ['Anyone wanna play league?',
                     'Anyone wanna play league? Also Im gay!',
                     'LEEEEEEEAAAAAAAAAAGUUUUUEEEEEEEEEEEEEEEEEEE',
                     'League? Doessssssss anyone wanna play?',
                     '¿Alguien quiere jugar a League of Legends?',
                     'S-spare league maam?',
                     'ITS LEAGUE!',
                     'I have no life and I dont expect you guys have one either, but I would like to willfully engage'
                     ' in some virtual combat where I play as a virtual avatar aka a champion,'
                     ' in which I smite other champions, sounds fun yes?',
                     'Anyone wanna play LEAGUE OF LOSERS?',
                     'Sex is overrated, lets play some league',
                     '?eugael yalp annaw enoynA',
                     'Ive run out of fuckin jokes. Give me some more. later kthnx',
                     'Anyone down for some league?',
                     'League of legends anyone?',
                     'Im down for some league, anyone else wanna play?',
                     'If your mmr is above room temperature, lets play some league']
        await ctx.send(f'@everyone {random.choice(responses)}')

    @commands.command()
    async def heroes(self, ctx):
        await ctx.send('@everyone HEEEERRRROOOOESSSSSS')

    # Annoy miguel, fix later :)
    @commands.command()
    async def annoyMiguel(self, ctx):
        for x in range(1):
            await ctx.send('https://www.youtube.com/watch?v=v5RZ8k6iQik, youre dead now!')

    # Magic 8Ball
    @commands.command(aliases=['8ball', 'test'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    # Sends file to chat
    @commands.command()
    async def send(self, ctx):
        """Sends an image. Need to work on this"""
        await ctx.send(file=discord.File('000.jpg'))

    # Sends mp3 to chat
    @commands.command()
    async def excision(self, ctx):
        """Sends an mp3 to the chat. Need to work on this"""
        await ctx.send(file=discord.File('Excision.mp3'))

    @commands.command()
    async def speech(self, ctx, *, name):
        tts = gTTS(f'{name}', lang="en-ie")
        tts.save(f'speech.mp3')
        await ctx.send(file=discord.File(f'speech.mp3'))

    @commands.command()
    async def rspeech(self, ctx, *, name):
        reverse = name[::-1]
        tts = gTTS(f'{reverse}')
        tts.save(f'reverse.mp3')
        await ctx.send(file=discord.File(f'reverse.mp3'))

    @commands.command()
    async def copyP(self, ctx):
        """Navy seals copypasta, but in an australian accent m8"""
        tts = gTTS(copypasta, lang="en-au")
        tts.save('hi.mp3')
        await ctx.send(file=discord.File('hi.mp3'))

    @commands.command()
    async def hug(self, ctx, *, user: discord.Member):
        await ctx.send(f"hug for {user.mention} :heart::heart::heart:")

    @commands.command()
    async def announce(self, ctx):
        """makes a minor announcement. No Sweat."""
        msg = ctx.message.content
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used):]

        # Next, we check if the user actually passed some text
        if text == '':
            # User didn't specify the text

            await ctx.send(content='You need to specify the text!')

            pass
        else:
            # User specified the text.
            await ctx.channel.purge(limit = 1)
            await ctx.send(content=f"**{text}**")

            pass

        return



def setup(commands):
    commands.add_cog(Example(commands))