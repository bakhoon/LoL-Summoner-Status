import discord
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from summonerInfo import getSummonerIdentification
from dotenv import load_dotenv
from champion import get_champion_info_embed
from ranked import init_tier, init_tier_embed, get_tiers_type, get_tier_info, get_max_tier, get_winratio
from summoner import get_summoner_info
import os

load_dotenv()

bot = commands.Bot(command_prefix = '.')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

guild_ids = [int(os.getenv('GUILD_ID'))]

@slash.slash(
    name="summoner",
    guild_ids=guild_ids, 
    options=[
        create_option(
            name="summoners_name",
            description="Insert summoner's name to view summoner's information",
            option_type=3,
            required=False,
        )
    ]
)
async def getSummonerInfo(ctx=SlashContext, summoners_name=None):

    summoner = getSummonerIdentification(summoners_name)
    
    summoner_name, summoner_level, summoner_url = get_summoner_info(summoner)

    ranked_solo_tier, ranked_solo_league_point, ranked_solo_wins, ranked_solo_losses, ranked_solo_winratio = init_tier()
    ranked_flex_tier, ranked_flex_league_point, ranked_flex_wins, ranked_flex_losses, ranked_flex_winratio = init_tier()

    tiers_type = get_tiers_type()

    for ranked_type in range(len(summoner['tier_info'])):
        if summoner['tier_info'][ranked_type]['queueType'] == 'RANKED_SOLO_5x5':
            ranked_solo_tier, ranked_solo_league_point, ranked_solo_wins, ranked_solo_losses = get_tier_info(summoner, ranked_type)
        elif summoner['tier_info'][ranked_type]['queueType'] == 'RANKED_FLEX_SR':
            ranked_flex_tier, ranked_flex_league_point, ranked_flex_wins, ranked_flex_losses = get_tier_info(summoner, ranked_type)
    
    if len(summoner['tier_info']) == 2:
        if tiers_type.index(summoner['tier_info'][0]['tier']) > tiers_type.index(summoner['tier_info'][0]['tier']):
            max_tiers = get_max_tier(summoner, 0, tiers_type)
        else:
            max_tiers = get_max_tier(summoner, 1, tiers_type)
    elif len(summoner['tier_info']) == 1:
        max_tiers = get_max_tier(summoner, 0, tiers_type)
    else:
        max_tiers = 'default'       

    embed_description_ranked_solo_tier, embed_description_ranked_solo_winratio, embed_description_ranked_flex_tier, embed_description_ranked_flex_winratio = init_tier_embed()

    if ranked_solo_wins > 0 and ranked_solo_losses > 0: 
        embed_description_ranked_solo_tier, embed_description_ranked_solo_winratio = get_winratio(ranked_solo_wins, ranked_solo_losses, ranked_solo_tier, ranked_solo_league_point)
    if ranked_flex_wins > 0 and ranked_flex_losses > 0: 
        embed_description_ranked_flex_tier, embed_description_ranked_flex_winratio = get_winratio(ranked_flex_wins, ranked_flex_losses, ranked_flex_tier, ranked_flex_league_point)

    embed_title = summoner_name + ' (Level ' + summoner_level + ')'
    embed_description = ''
    if embed_description_ranked_solo_tier == '' and embed_description_ranked_flex_tier == '':
        embed_description = 'Ranked Tier: Unranked'
    elif embed_description_ranked_solo_tier != '' and embed_description_ranked_flex_tier == '':
        embed_description = embed_description_ranked_solo_tier + '\r\n' + embed_description_ranked_solo_winratio
    elif embed_description_ranked_solo_tier == '' and embed_description_ranked_flex_tier != '':
        embed_description = embed_description_ranked_flex_tier + '\r\n' + embed_description_ranked_flex_winratio
    else:
        embed_description = embed_description_ranked_solo_tier + '\r\n' + embed_description_ranked_solo_winratio + ' \r\n\r\n' + embed_description_ranked_flex_tier + '\r\n' + embed_description_ranked_flex_winratio
    
    embed = discord.Embed(title=embed_title, description=embed_description, colour=discord.Colour.blue(), url=summoner_url)
    embed.set_thumbnail(url='https://opgg-static.akamaized.net/images/medals/' + max_tiers + '.png?image=q_auto:best&v=1')
    
    embeds = [embed]

    for champion_type in ['champion_mastery_info','champion_recent_info']:
        for champion in summoner[champion_type]:
            embed = get_champion_info_embed(summoner, champion, embeds, champion_type)

    await ctx.send(embeds=embeds)

bot.run(os.getenv('BOT'))

