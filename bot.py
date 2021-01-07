import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
import nacl

from bs4 import BeautifulSoup
import requests

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = ".", help_command=None)


@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')

@client.event
async def on_ready():
    print('aye aye captain')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the sun rise 🧘'))

@client.command()
async def help(ctx):
    await ctx.send("Look towards the light and ask. `.meditate`.")

@client.command(aliases=['zen', 'meditate'])
async def motivate(ctx):
    res = requests.get('https://inspirobot.me/api?generate=true')
    
    if (res.status_code == requests.codes.ok):
        await ctx.send(res.text)
    else:
        await ctx.send("Tranquility not yet available.")

@client.command(aliases=['gm','guide','guided','guidedmeditation'])
async def guidedMeditation(ctx):
    id = requests.get('https://inspirobot.me//api?getSessionID=1').text
    res = requests.get('https://inspirobot.me/api?generateFlow=1&sessionID='+id)

    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()
    
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    audio_source = discord.FFmpegPCMAudio(res.json()['mp3'])
    voice.play(audio_source,after=None)
  
    print(id)
client.run(token)