import discord
from discord.ext import commands
import requests
import urllib
import os

temp = open("password.txt", 'r')
userAgent ='Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36'

username = 'mrcallus'
password = temp.read()
temp.close()

if os.stat("memeIDs.txt").st_size == 0:
    memeFile = open("memeIDs.txt", "w")
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
    ctr = 1
    for img in images:
        imageName = str(ctr) + ' ' + img['name']
        memeFile.write(imageName + "\n")
        ctr = ctr + 1
    memeFile.close()



class meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    def memeIDList(self):
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
        return images

    @commands.command()
    async def meme(self, ctx, *, meme):
        if not meme:
            await ctx.send("Empty!")
        if meme == "help":
            await ctx.send("This is a meme maker. Here is a list of memes you can make. Ex. Meme ID: top text, bottom text.")
            await ctx.send("Help is on the way!!2")
            memeFile = open("memeIDs.txt", "r")
            idString = ""
            for x in memeFile:
                idString = idString  + x
                if len(idString) > 1975:
                    break
            memeFile.close()
            await ctx.send(idString)
        #await ctx.send(file=discord.File('000.jpg'))
        #If null embed help
        #if list return list
        #Separate by comma?? Bottom/Top Test
        #Save as a meme.jpg, for override

def setup(client):
    client.add_cog(meme(client))