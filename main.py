import discord
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from summonerInfo import getSummonerIdentification
from dotenv import load_dotenv
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
    
    summoner_name:str = summoner['summoner_info']['name']
    summoner_level:str = str(summoner['summoner_info']['summonerLevel'])
    summoner_url:str = 'https://na.op.gg/summoner/userName=' + summoner_name.replace(" ", "")

    ranked_solo_tier:str = ''
    ranked_solo_league_point:int = 0
    ranked_solo_wins:int = 0
    ranked_solo_losses:int = 0

    ranked_flex_tier:str = ''
    ranked_flex_league_point:int = 0
    ranked_flex_wins:int = 0
    ranked_flex_losses:int = 0

    ranked_solo_winratio:float = 0.0
    ranked_flex_winratio:float = 0.0

    tiers_type = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
    max_tiers = ''

    for ranked_type in range(len(summoner['tier_info'])):
        if summoner['tier_info'][ranked_type]['queueType'] == 'RANKED_SOLO_5x5':
            ranked_solo_tier = summoner['tier_info'][ranked_type]['tier'] + ' ' + summoner['tier_info'][ranked_type]['rank']
            ranked_solo_league_point = summoner['tier_info'][ranked_type]['leaguePoints']
            ranked_solo_wins = summoner['tier_info'][ranked_type]['wins']
            ranked_solo_losses = summoner['tier_info'][ranked_type]['losses']
        elif summoner['tier_info'][ranked_type]['queueType'] == 'RANKED_FLEX_SR':
            ranked_flex_tier = summoner['tier_info'][ranked_type]['tier'] + ' ' + summoner['tier_info'][ranked_type]['rank']
            ranked_flex_league_point = summoner['tier_info'][ranked_type]['leaguePoints']
            ranked_flex_wins = summoner['tier_info'][ranked_type]['wins']
            ranked_flex_losses = summoner['tier_info'][ranked_type]['losses']
    
    if len(summoner['tier_info']) == 2:
        if tiers_type.index(summoner['tier_info'][0]['tier']) > tiers_type.index(summoner['tier_info'][0]['tier']):
            if summoner['tier_info'][ranked_type]['rank'] == "I":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_1'
            elif summoner['tier_info'][ranked_type]['rank'] == "II":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_2'
            elif summoner['tier_info'][ranked_type]['rank'] == "III":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_3'
            elif summoner['tier_info'][ranked_type]['rank'] == "IV":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_4'
        else:
            if summoner['tier_info'][ranked_type]['rank'] == "I":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][1]['tier'])] + '_1'
            elif summoner['tier_info'][ranked_type]['rank'] == "II":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][1]['tier'])] + '_2'
            elif summoner['tier_info'][ranked_type]['rank'] == "III":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][1]['tier'])] + '_3'
            elif summoner['tier_info'][ranked_type]['rank'] == "IV":
                max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][1]['tier'])] + '_4'
    elif len(summoner['tier_info']) == 1:
        if summoner['tier_info'][ranked_type]['rank'] == "I":
            max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_1'
        elif summoner['tier_info'][ranked_type]['rank'] == "II":
            max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_2'
        elif summoner['tier_info'][ranked_type]['rank'] == "III":
            max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_3'
        elif summoner['tier_info'][ranked_type]['rank'] == "IV":
            max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][0]['tier'])] + '_4'
    else:
        max_tiers = 'default'       

    embed_description_ranked_solo_tier:str = ''
    embed_description_ranked_solo_winratio:str = ''
    embed_description_ranked_flex_tier:str = ''
    embed_description_ranked_flex_winratio:str = ''

    if ranked_solo_wins > 0 and ranked_solo_losses > 0: 
        ranked_solo_winratio = "%.2f" % (float(ranked_solo_wins)*100/(float(ranked_solo_wins)+float(ranked_solo_losses)))
        embed_description_ranked_solo_tier = 'Ranked Solo Tier: ' + ranked_solo_tier + ' ' + str(ranked_solo_league_point) + ' LP'
        embed_description_ranked_solo_winratio = 'Ranked Solo Win Ratio: ' + str(ranked_solo_winratio) + '% (' + str(ranked_solo_wins) + 'W - ' + str(ranked_solo_losses) + 'L)'
    if ranked_flex_wins > 0 and ranked_flex_losses > 0: 
        ranked_flex_winratio = "%.2f" % (float(ranked_flex_wins)*100/(float(ranked_flex_wins)+float(ranked_flex_losses)))
        embed_description_ranked_flex_tier = 'Ranked Flex Tier: ' + ranked_flex_tier + ' ' + str(ranked_flex_league_point) + ' LP'
        embed_description_ranked_flex_winratio = 'Ranked Flex Win Ratio: ' + str(ranked_flex_winratio) + '% (' + str(ranked_flex_wins) + 'W - ' + str(ranked_flex_losses) + 'L)'

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

    for champion in summoner['champion_mastery_info']:
        
        last_play_time = datetime.fromtimestamp(champion['lastPlayTime']/1000)
        champion_description = "Champion Points: " + str(champion['championPoints']) + '\r\n' + "Champion Last Played: " + str(last_play_time)
        champion_name = summoner['champion_list'][str(champion['championId'])] + ' (Level ' + str(champion['championLevel']) + ')'
        champion_url = "https://na.op.gg/champion/" + summoner['champion_list'][str(champion['championId'])] + "/"
        champion_icon_url = 'https://opgg-static.akamaized.net/images/lol/champion/' + summoner['champion_list'][str(champion['championId'])] + '.png?image=c_scale,q_auto,w_40'
        champion_embed = discord.Embed(description=champion_description, colour=discord.Colour.gold())
        champion_embed.set_author(name=champion_name, url=champion_url, icon_url=champion_icon_url)
        embeds.append(champion_embed)
    
    for champion in summoner['champion_recent_info']:
        
        last_play_time = datetime.fromtimestamp(champion['lastPlayTime']/1000)
        champion_description = "Champion Points: " + str(champion['championPoints']) + '\r\n' + "Champion Last Played: " + str(last_play_time)
        champion_name = summoner['champion_list'][str(champion['championId'])] + ' (Level ' + str(champion['championLevel']) + ')'
        champion_url = "https://na.op.gg/champion/" + summoner['champion_list'][str(champion['championId'])] + "/"
        champion_icon_url = 'https://opgg-static.akamaized.net/images/lol/champion/' + summoner['champion_list'][str(champion['championId'])] + '.png?image=c_scale,q_auto,w_40'
        champion_embed = discord.Embed(description=champion_description, colour=discord.Colour.dark_orange())
        champion_embed.set_author(name=champion_name, url=champion_url, icon_url=champion_icon_url)
        embeds.append(champion_embed)

    await ctx.send(embeds=embeds)

bot.run(os.getenv('BOT'))