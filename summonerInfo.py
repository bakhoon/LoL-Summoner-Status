
from riotwatcher import LolWatcher
from dotenv import load_dotenv
import os

load_dotenv()

lol_watcher = LolWatcher(os.getenv('LOL_WATCHER'))

summoner_ID = 'liveevil'
region = 'na1'
region_v5 = 'AMERICAS'

def getSummonerIdentification(summoner_ID):
    summoner = {}
    champion_list = {}

    summoner_info = lol_watcher.summoner.by_name(region, summoner_ID)
    champion_info = lol_watcher.champion_mastery.by_summoner(region, summoner_info['id'])
    tier_info = lol_watcher.league.by_summoner(region, summoner_info['id'])
    version_list = lol_watcher.data_dragon.versions_for_region(region)
    champion_json = lol_watcher.data_dragon.champions(version_list['v'])

    for champion in champion_json['data'].keys():
        champion_list[champion_json['data'][champion]['key']] = champion

    summoner['summoner_info'] = summoner_info
    summoner['champion_list'] = champion_list
    if len(champion_info) > 5:
        summoner['champion_mastery_info'] = champion_info[:4]
    else:
        summoner['champion_mastery_info'] = champion_info
    summoner['tier_info'] = tier_info
    
    champion_info.sort(key=recentPlayTime, reverse=True)

    if len(champion_info) > 5:
        summoner['champion_recent_info'] = champion_info[:4]
    else:
        summoner['champion_recent_info'] = champion_info

    return summoner


def recentPlayTime(key):
    return key['lastPlayTime']


