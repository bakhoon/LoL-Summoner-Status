import discord
import requests
import json
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def say(message):
    await message.send("I hate you!")

bot.run('ODY4MjYyODU1MDM0Njk5ODA2.YPtGzA.dRKN9whwiUSHHYBQ6TX-EZsjp48')