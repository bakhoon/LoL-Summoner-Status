import discord
from datetime import datetime

def get_champion_info_embed(summoner, champion, embeds, champion_type):
    last_play_time = datetime.fromtimestamp(champion['lastPlayTime']/1000)
    champion_description = "Champion Points: " + str(champion['championPoints']) + '\r\n' + "Champion Last Played: " + str(last_play_time)
    champion_name = summoner['champion_list'][str(champion['championId'])] + ' (Level ' + str(champion['championLevel']) + ')'
    champion_url = "https://na.op.gg/champion/" + summoner['champion_list'][str(champion['championId'])] + "/"
    champion_icon_url = 'https://opgg-static.akamaized.net/images/lol/champion/' + summoner['champion_list'][str(champion['championId'])] + '.png?image=c_scale,q_auto,w_40'
    
    if champion_type == 'champion_mastery_info':
        champion_embed = discord.Embed(description=champion_description, colour=discord.Colour.gold())
    else:
        champion_embed = discord.Embed(description=champion_description, colour=discord.Colour.dark_green())
    
    champion_embed.set_author(name=champion_name, url=champion_url, icon_url=champion_icon_url)
    embeds.append(champion_embed)
    
    return embeds