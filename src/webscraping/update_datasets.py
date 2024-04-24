from scrap_leagues import GetData

league_list = ['br', 'en', 'it', 'es', 'de', 'fr']

for league in league_list:
  if league == 'br':
    league = GetData(league, '2014')
  else:
    league = GetData(league, '2014-2015')
  
  #league.get_standings(has_downloaded=False)
  #league.get_standings(has_downloaded=True)
  league.get_match_history(has_downloaded=False)
  #league.get_match_history(has_downloaded=True)
  #league.get_squads(has_downloaded=False)
  #league.get_squads(has_downloaded=True)
