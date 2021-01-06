import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

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

client.run(token)
