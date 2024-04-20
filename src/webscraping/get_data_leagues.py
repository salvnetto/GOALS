import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

from ..utils import helper_webscrap
from . import URL_FBREF


class GetDataLeagues:
  def __init__(self, league, season):
    match league:
      case 'br':
        self.name = 'Brasileirao'
        self.url = URL_FBREF + f'/en/comps/24/{season}/{season}-Serie-A-Stats'
        self.data_path = '../datasets/raw_data/brasileirao/'
      case 'en':
        self.name = 'Premier League'
        self.url = URL_FBREF + f'/en/comps/9/{season}/{season}-Premier-League-Stats'
        self.data_path = '../datasets/raw_data/premier_league/'
      case 'it':
        self.name = 'Serie A'
        self.url = URL_FBREF + f'/en/comps/11/{season}/{season}-Serie-A-Stats'
        self.data_path = '../datasets/raw_data/serie_a/'
      case 'es':
        self.name = 'La Liga'
        self.url = URL_FBREF + f'/en/comps/12/{season}/{season}-La-Liga-Stats'
        self.data_path = '../datasets/raw_data/la_liga/'
      case 'de':
        self.name = 'Bundesliga'
        self.url = URL_FBREF + f'/en/comps/20/{season}/{season}-Bundesliga-Stats'
        self.data_path = '../datasets/raw_data/bundesliga/'
      case 'fr':
        self.name = 'Ligue 1'
        self.url = URL_FBREF + f'/en/comps/13/{season}/{season}-Ligue-1-Stats'
        self.data_path = '../datasets/raw_data/ligue_1/'

    self.season = season
    self.data_raw = requests.get(self.url)
    self.soup = BeautifulSoup(self.data_raw.text)

  def __extract_teams_url(self):
    table = self.soup.select('table.stats_table')[0]
    links = table.find_all('a')
    links = [link.get('href') for link in links]
    links = [link for link in links if '/squads/' in link]
    urls = [f"{URL_FBREF}{link}" for link in links]

    return urls

  def __get_prev_season(self):
    try:
      prev_season = self.soup.select('a.prev')[0].get('href')
      league_url = URL_FBREF + prev_season
    except IndexError:
      pass

    return league_url
  
  def get_standings(self, seasons):
    data = pd.read_feather(self.data_path + 'standings.fea')
    
    #if data['aux_download'] 
    data = self.data_raw.text
    for season in seasons:
      standing = pd.read_html(data, match= 'Regular season')[0]
      standing['season'] = season
      standing['league_name'] = self.name
      standings.append(standings)


