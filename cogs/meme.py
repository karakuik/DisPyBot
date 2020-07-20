import discord
from discord.ext import commands
import requests
import urllib
import os
import os.path

temp = open("password.txt", 'r')
userAgent ='Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36'

username = 'mrcallus'
password = temp.read()
temp.close()

directory = '/home/pi/PycharmProjects/DiscordBot/TextFiles/'
filename = "memeIDs.txt"
file_path = os.path.join(directory, filename)
file = open(file_path, "w")
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
ctr = 1
for img in images:
    imageName = str(ctr) + ' ' + img['name']
    file.write(imageName + "\n")
    ctr = ctr + 1
file.close()


class meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    def memeIDList(self):
        data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
        images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
        return images


    @commands.command(description = "Creates a meme for the chat. EX: .meme 1, Hello, World!")
    async def meme(self, ctx, *, meme):
        """Makes a meme use num, topline, bottomline *include commas!"""
        if not meme:
            await ctx.send("Empty!")
        if meme == "help":
            await ctx.send("Help is on the way!!1!1")
            memeFile = open("TextFiles/memeIDs.txt", "r")
            idString = ""
            for x in memeFile:
                idString = idString + x
                if len(idString) > 1975:
                    await ctx.send(idString)
                    idString = ""
            memeFile.close()
            await ctx.send(idString)
            await ctx.send("Send in the format of .meme num, topline, bottomline")
            await ctx.send("I separate using commas so be sure to add those until i figure out a better way :joy:")
        else:
            data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
            images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
            memeID = meme.split(", ")
            id = int(memeID[0])
            text0 = memeID[1]
            text1 = memeID[2]
            URL = 'https://api.imgflip.com/caption_image'
            params = {
                'username': username,
                'password': password,
                'template_id': images[id - 1]['id'],
                'text0': text0,
                'text1': text1
            }
            response = requests.request('POST', URL, params=params).json()
            print(response)

            # Save the meme
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', userAgent)
            filename, headers = opener.retrieve(response['data']['url'], images[id - 1]['name'] + '.jpg')
            await ctx.send(file = discord.File(images[id - 1]['name'] + '.jpg'))

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found.\nEnter like this: .meme 1, Top Text, Bottom Text")

def setup(client):
    client.add_cog(meme(client))