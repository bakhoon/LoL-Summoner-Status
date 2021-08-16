def init_tier() -> list[str]:
    ranked_tier:str = ''
    ranked_league_point:int = 0
    ranked_wins:int = 0
    ranked_losses:int = 0
    ranked_winratio:float = 0.0
    
    return [ranked_tier, ranked_league_point, ranked_wins, ranked_losses, ranked_winratio]

def init_tier_embed() -> list[str]:
    embed_description_ranked_solo_tier:str = ''
    embed_description_ranked_solo_winratio:str = ''
    embed_description_ranked_flex_tier:str = ''
    embed_description_ranked_flex_winratio:str = ''
    
    return [embed_description_ranked_solo_tier, embed_description_ranked_solo_winratio, embed_description_ranked_flex_tier, embed_description_ranked_flex_winratio]

def get_tiers_type() -> list[str]:
    
    return ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']

def get_tier_info(summoner, ranked_type) -> list:
    ranked_tier = summoner['tier_info'][ranked_type]['tier'] + ' ' + summoner['tier_info'][ranked_type]['rank']
    ranked_league_point = summoner['tier_info'][ranked_type]['leaguePoints']
    ranked_wins = summoner['tier_info'][ranked_type]['wins']
    ranked_losses = summoner['tier_info'][ranked_type]['losses']
    
    return [ranked_tier, ranked_league_point, ranked_wins, ranked_losses]

def get_max_tier(summoner, ranked_type, max_tiers) -> str:

    tiers_type = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']

    if summoner['tier_info'][ranked_type]['rank'] == "I":
        max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][ranked_type]['tier'])] + '_1'
    elif summoner['tier_info'][ranked_type]['rank'] == "II":
        max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][ranked_type]['tier'])] + '_2'
    elif summoner['tier_info'][ranked_type]['rank'] == "III":
        max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][ranked_type]['tier'])] + '_3'
    elif summoner['tier_info'][ranked_type]['rank'] == "IV":
        max_tiers = tiers_type[tiers_type.index(summoner['tier_info'][ranked_type]['tier'])] + '_4'
    
    return max_tiers

def get_winratio(ranked_wins, ranked_losses, ranked_tier, ranked_league_point) -> list[str]:
    if ranked_wins > 0 and ranked_losses > 0: 
        ranked_winratio = "%.2f" % (float(ranked_wins)*100/(float(ranked_wins)+float(ranked_losses)))
        embed_description_ranked_tier = 'Ranked Solo Tier: ' + ranked_tier + ' ' + str(ranked_league_point) + ' LP'
        embed_description_ranked_winratio = 'Ranked Solo Win Ratio: ' + str(ranked_winratio) + '% (' + str(ranked_wins) + 'W - ' + str(ranked_losses) + 'L)'
    
    return [embed_description_ranked_tier, embed_description_ranked_winratio]