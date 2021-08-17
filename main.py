from discord.ext import commands

from decouple import config

bot = commands.Bot(command_prefix = '.')

for cog in ['initialization', 'getSummonerInfo']:
    bot.load_extension(f'cogs.{cog}')

bot.run(config('BOT'))

