import discord
from discord.ext import commands
from datetime import *

class Terminate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def terminate(self, ctx):
        """Terminates the bot. Only to be used by me muthafucka"""
        x = datetime.now()
        print(x.strftime("\n\n Teminated at:\t %m/%d/%Y, %H:%M:%S\n\n"))
        my_file = open("Log.txt", "a")
        my_file.write(x.strftime("Terminated at:\t %m/%d/%Y, %H:%M:%S\n"))
        my_file.close()
        await ctx.send(x.strftime("Terminating the bot. Time Logged @ \t%m/%d/%Y, %H:%M:%S"))
        exit()

def setup(client):
  client.add_cog(Terminate(client))