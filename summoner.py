def get_summoner_info(summoner) -> list[str]:
    summoner_name:str = summoner['summoner_info']['name']
    summoner_level:str = str(summoner['summoner_info']['summonerLevel'])
    summoner_url:str = 'https://na.op.gg/summoner/userName=' + summoner_name.replace(" ", "")
    return [summoner_name, summoner_level, summoner_url]