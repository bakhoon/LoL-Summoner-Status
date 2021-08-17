import os
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix = '.')

for cog in ['initialization', 'getSummonerInfo']:
    bot.load_extension(f'cogs.{cog}')

bot.run(os.getenv('BOT'))

