from unidecode import unidecode



def accent_remover(text):
    return unidecode(text)


def get_season_text(soup):
  season_text = soup.find_all('h1')
  season_text = [i.get_text(strip= True) for i in season_text]
  season = season_text[0].split(" ")[0]

  return season


def get_prev_season(soup, league_url, year):
  try:
    prev_season = soup.select('a.prev')[0].get('href')
    league_url = f"https://fbref.com{prev_season}"
  except IndexError:
    print('*Error: ', year)

  return league_url
  