from webscraping.get_data_leagues import GetLeagueData

league_list = ['br', 'en', 'it', 'es', 'de', 'fr']

for league in league_list:
  if league == 'br':
    league = GetLeagueData(league, '2014')
  else:
    league = GetLeagueData(league, '2014-2015')
  
  #league.get_standings(has_downloaded=False)
  league.get_standings(has_downloaded=True)