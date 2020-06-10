import discord
from discord.ext import commands

class Test(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def tester(self, ctx):
    await ctx.send('tester')

  @commands.command()
  async def ding(self, ctx):
    await ctx.send('Dong from Test.cog!')

def setup(client):
  client.add_cog(Test(client))