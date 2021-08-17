from discord.ext import commands

class Initialization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

def setup(bot):
    bot.add_cog(Initialization(bot))