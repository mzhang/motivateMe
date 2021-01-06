import os
import discord
from discord.ext import commands

token="Nzk2NDczODU5Mjc2NDA2ODA0.X_YcFQ.CtaZt53bG4EzEGfAIctOckQTCYs"
client = commands.Bot(command_prefix = ".", help_command=None)

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')


client.run(token)
