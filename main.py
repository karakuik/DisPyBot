import discord
import random
from discord.ext import commands
from gtts import gTTS
from copypasta import copypasta
import asyncio
import os
import datetime

client = commands.Bot(command_prefix='.')


hiddenFile = open("APISecret.txt", 'r')
APIKey = hiddenFile.read()
hiddenFile.close()

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx):
  await ctx.send('Reloading cogs')
  for cog_filename in os.listdir('./cogs'):
      if cog_filename.endswith('.py'):
          print(f'cogs.{cog_filename[:-3]}')
          client.unload_extension(f'cogs.{cog_filename[:-3]}')
  for cog_filename in os.listdir('./cogs'):
      if cog_filename.endswith('.py'):
          print(f'cogs.{cog_filename[:-3]}')
          client.load_extension(f'cogs.{cog_filename[:-3]}')

@client.event
async def on_ready():
    x = datetime.datetime.now()
    servers = list(client.guilds)
    print(x.strftime("Started at:\t %m/%d/%Y, %H:%M:%S\n\n"))
    my_file = open("TextFiles/Log.txt", "a")
    my_file.write(x.strftime("Started at:\t %m/%d/%Y, %H:%M:%S\n"))
    my_file.write(f'Logged in as {client.user.name} - {client.user.id}\n')
    my_file.write("Connected to: + " + str(len(client.guilds)) + " Servers:")
    for x in range(len(servers)):
        my_file.write(' ' + servers[x - 1].name + ',')
    my_file.write("\n\n")
    my_file.close()
    for file in os.listdir("."):
        if (os.path.isfile(file) and file.startswith("youtube")) or (os.path.isfile(file) and file.endswith(".jpg")):
            try:
                os.remove(file)
            except e:
                print(e)

    print("Connected on " + str(len(client.guilds)) + " servers: ")
    for x in range(len(servers)):
        print(' ' + servers[x-1].name)
    print(f'Logged in as {client.user.name} - {client.user.id}')


@client.event
async def on_member_join(member):
    x = datetime.datetime.now()
    my_file = open("TextFiles/User_Log.txt", "a")
    my_file.write(x.strftime(f"{member} joined at:\t %m/%d/%Y, %H:%M:%S\n\n"))
    my_file.close()
    print(f'{member} has joined a server.')


@client.event
async def on_member_remove(member):
    x = datetime.datetime.now()
    my_file = open("TextFiles/User_Log.txt", "a")
    my_file.write(x.strftime(f"{member} left at:\t %m/%d/%Y, %H:%M:%S\n\n"))
    my_file.close()
    print(f'{member} has left the server')


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content == "oof":
        await message.channel.send("foo")
        await asyncio.sleep(5)  # This will let it sleep, u can still do commands
        await message.channel.send("bar!")
    elif message.content == ":D":
        await message.channel.send(":D")
        # await message.author.send('👋') #This sends me a wave

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass all required arguments.\nUse help for more info")

@client.command
async def test_Command(ctx, str):
    await ctx.send(str);

#@test_Command.error
#async def meme_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send("No arguments found.\nEnter like this: .meme 1, Top Text, Bottom Text")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    print(f'cogs.{filename[:-3]}')
    if filename[:-3] == "terminate":
        continue
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(APIKey)