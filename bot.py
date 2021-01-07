import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
import nacl

from bs4 import BeautifulSoup
import requests

import asyncio

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
    embed=discord.Embed(title="To those who seek guidance:")
    embed.add_field(name="Motivation comes at a cost. ", value="The cost of you typing `.motivate`. Or `.zen`.", inline=False)
    embed.add_field(name="Inner piece takes time. And guidance.", value="Think to yourself: `.meditate`. Concentrate. Focus. Then type `.meditate`.", inline=False)
    embed.set_footer(text="Not all who are lost are wanderers. ")
    await ctx.send(embed=embed)

@client.command(aliases=['zen'])
async def motivate(ctx):
    res = requests.get('https://inspirobot.me/api?generate=true')
    
    if (res.status_code == requests.codes.ok):
        await ctx.send(res.text)
    else:
        await ctx.send("Tranquility not yet available in your area. .")
        
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    await voice.disconnect()

def play(voice, id):
    res = requests.get('https://inspirobot.me/api?generateFlow=1&sessionID='+id)
    audio_source = discord.FFmpegPCMAudio(res.json()['mp3'])
    print(len(voice.channel.members))
    if len(voice.channel.members) == 1:
        print('leaving!' + str(voice.channel.members))
        coroutine = voice.disconnect()
        future = asyncio.run_coroutine_threadsafe(coroutine, client.loop)
        try:
            future.result()
        except:
            print('future.result() failed!')
            pass
    print('play start!')
    voice.play(audio_source, after=lambda e: play(voice, id))
    

@client.command(aliases=['gm','meditate','guided','guidedmeditation'])
async def guidedMeditation(ctx):
    id = requests.get('https://inspirobot.me/api?getSessionID=1').text

    try: 
        channel = ctx.author.voice.channel
    except:
        await ctx.send("Steady yourself. Connect to voice.")
        return

    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Close your eyes. Focus. Breathe.")

    res = requests.get('https://inspirobot.me/api?generateFlow=1&sessionID='+id)
    audio_source = discord.FFmpegPCMAudio(res.json()['mp3'])
    voice.play(audio_source, after=lambda e: play(voice, id))

client.run(token)