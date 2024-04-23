import requests
import warnings
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

warnings.simplefilter(action='ignore', category=FutureWarning)

from .constants import *
from .process_data import process_match_history, process_standing, process_squads

class GetData:
  """Class to fetch and manage data from various football leagues.

  Attributes:
  -----------
  league : str
    The abbreviation code of the league (e.g., 'br' for Brasileirao).
    Supported leagues and their codes:
      'br' - Brasileirao (Brazilian League)
      'en' - Premier League (English League)
      'it' - Serie A (Italian League)
      'es' - La Liga (Spanish League)
      'de' - Bundesliga (German League)
      'fr' - Ligue 1 (French League)
  first_season : str
    The starting season for which data is to be fetched. 
    Format: 'YYYY' for single year or 'YYYY-YYYY' for a range, depending on the region.

  Methods:
  --------
  get_standings(has_downloaded=True):
    Fetches standings data for the league, optionally downloads it if not already downloaded.
  get_match_history(has_downloaded=True):
    Fetches match history per team in the league, optionally downloads it if not already downloaded.
  get_squads(has_downloaded=True):
    Fetches squads players data for the teams in the league, optionally downloads it if not already downloaded.
  """

  def __init__(self, league, first_season):
    self.league = league
    self.first_season = first_season
    self._set_league_properties()
    self._initialize_data()

  def _set_league_properties(self):
    leagues = {
        'br': ('Brasileirao', '24'),
        'en': ('Premier League', '9'),
        'it': ('Serie A', '11'),
        'es': ('La Liga', '12'),
        'de': ('Bundesliga', '20'),
        'fr': ('Ligue 1', '13')
    }
    if self.league in leagues:
        self.name, self.league_id = leagues[self.league]
        self.url = f"{URL_FBREF}/en/comps/{self.league_id}/{self.first_season}/{self.first_season}-{self.name.replace(' ', '-')}-Stats"
        self.league_code = self.name.lower().replace(' ', '_')
        self.data_path = f"datasets/raw_data/{self.league_code}/"
        now = datetime.now()
        if self.league == 'br':
          SEASONS_LIST.append(str(now.year))
        else:
          if now.month < 7:
            current_year = str(now.year)
            if current_year in SEASONS_LIST:
              SEASONS_LIST.remove(current_year)
    else:
        raise ValueError(f"League '{self.league}' not supported.")

  def _initialize_data(self):
      self.data_initial = requests.get(self.url)
      self.soup_initial = BeautifulSoup(self.data_initial.text, features="lxml")

  def _get_url_teams(self, url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features= 'lxml')
    table = soup.select('table.stats_table')[0]           
    links = table.find_all('a')                           
    links = [link.get('href') for link in links]          
    links = [link for link in links if '/squads/' in link]  
    urls = [f"https://fbref.com{link}" for link in links]

    return urls
  
  def _get_team_match_history(self, season, urls):
    match_history = []
    for team in urls:
      team_name = team.split('/')[-1].replace('-Stats', '').replace('-','_').lower()
      team_mh = pd.read_html(team)[1]
      team_mh['season'] = season
      team_mh['league_id'] = self.league_id
      team_mh['league_name'] = self.name
      team_mh['team'] = team_name
      print(f'--{team_name}')

      data = requests.get(team)
      soup = BeautifulSoup(data.text, features= 'lxml')
      anchor = [link.get("href") for link in soup.find_all('a')]
      ##Shooting
      try:
        links = [l for l in anchor if l and 'all_comps/shooting/' in l]
        shooting = pd.read_html(f"https://fbref.com{links[0]}")[0]
        shooting.columns = shooting.columns.droplevel()
        team_mh = team_mh.merge(shooting[['Date', 'Sh', 'SoT']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Goalkeeping
      try:
        links = [l for l in anchor if l and 'all_comps/keeper' in l]
        goalkeeping = pd.read_html(f"https://fbref.com{links[0]}")[0]
        goalkeeping.columns = goalkeeping.columns.droplevel()
        team_mh = team_mh.merge(goalkeeping[['Date', 'Saves']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Passing
      try:
        links = [l for l in anchor if l and 'all_comps/passing' in l]
        passing = pd.read_html(f"https://fbref.com{links[0]}")[0]
        passing.columns = passing.columns.droplevel()
        team_mh = team_mh.merge(passing[['Date', 'Cmp', 'Att', 'PrgP', 'KP', '1/3']], on= 'Date')
        team_mh.rename(columns={'1/3': 'pass_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass
      ##Passing Types
      try:
        links = [l for l in anchor if l and 'all_comps/passing_types' in l]
        pass_types = pd.read_html(f"https://fbref.com{links[0]}")[0]
        pass_types.columns = pass_types.columns.droplevel()
        team_mh = team_mh.merge(pass_types[['Date', 'Sw', 'Crs']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Goal and Shot Creation
      try:
        links = [l for l in anchor if l and 'all_comps/gca' in l]
        goal_shotcreation = pd.read_html(f"https://fbref.com{links[0]}")[0]
        goal_shotcreation.columns = goal_shotcreation.columns.droplevel()
        team_mh = team_mh.merge(goal_shotcreation[['Date', 'SCA', 'GCA']], on= 'Date')
      except (ValueError, IndexError):
        pass
      ##Defense
      try:
        links = [l for l in anchor if l and 'all_comps/defense' in l]
        defensive = pd.read_html(f"https://fbref.com{links[0]}")[0]
        defensive.columns = defensive.columns.droplevel()
        team_mh = team_mh.merge(defensive[['Date', 'Tkl', 'TklW', 'Def 3rd', 'Att 3rd', 'Blocks', 'Int']], on= 'Date')
        team_mh.rename(columns={'Att 3rd': 'Tkl_Att_3rd',
                                'Def 3rd': 'Tkl_Def_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass
      ##Possession
      try:
        links = [l for l in anchor if l and 'all_comps/possession' in l]
        possession = pd.read_html(f"https://fbref.com{links[0]}")[0]
        possession.columns = possession.columns.droplevel()
        team_mh = team_mh.merge(possession[['Date', 'Att 3rd']], on= 'Date')
        team_mh.rename(columns={'Att 3rd': 'Touches_Att_3rd'}, inplace=True)
      except (ValueError, IndexError):
        pass

      ##Misc
      try:
        links = [l for l in anchor if l and 'all_comps/misc' in l]
        misc = pd.read_html(f"https://fbref.com{links[0]}")[0]
        misc.columns = misc.columns.droplevel()
        if 'Recov' not in misc.columns:
          misc['Recov'] = None
        team_mh = team_mh.merge(misc[['Date', 'Fls', 'Off', 'Recov']], on= 'Date')
      except (ValueError, IndexError):
        pass

      match_history.append(team_mh)
      time.sleep(1)
    match_history = pd.concat(match_history)

    return match_history

  def get_standings(self, has_downloaded=True):
    """Fetch standings data for the league.

    Parameters:
    -----------
    has_downloaded : bool, optional
        Flag indicating if data has already been downloaded. Defaults to True.
    """
    if has_downloaded is False:
      standing = pd.read_html(self.data_initial.text, match= 'Regular season')[0]
      standing['season'] = self.first_season
      standing['league_name'] = self.name
      standing['league_id'] = self.league_id
      if not os.path.exists(self.data_path):
        os.makedirs(self.data_path)
      print(f'{self.name} - {self.first_season} ({self.data_path})')
      standing.to_feather(self.data_path + 'standing.fea')

    if has_downloaded is True:
      standing_downloaded = pd.read_feather(self.data_path + 'standing.fea')
      downloaded_seasons = standing_downloaded['season'].unique()
      downloaded_seasons = [season.split('-')[0] for season in downloaded_seasons]
      
      for season in SEASONS_LIST:
        if season not in downloaded_seasons:
          if self.league in ('br'):
            season = season
          else:
            next_year = int(season) + 1
            season = f"{season}-{next_year}"
          url = self.url
          init_season = url.split('/')[6]
          url = url.replace(init_season, season)
          print(f'{self.name} - {season} ({self.data_path})')
          try:
            self.data = requests.get(url)
            standing = pd.read_html(self.data.text, match= 'Regular season')[0]
            standing['season'] = season
            standing['league_name'] = self.name
            standing['league_id'] = self.league_id
            standing_downloaded = pd.concat([standing_downloaded, standing])
            standing_downloaded.to_feather(self.data_path + 'standing.fea')
          except Exception as e:
            warnings.warn(f"Error while downloading data for season {season}: {e}")
            continue
        time.sleep(2)
    process_standing(self.league_code)

  def get_match_history(self, has_downloaded=True):
    """Fetch match history per team in the league.

    Parameters:
    -----------
    has_downloaded : bool, optional
        Flag indicating if data has already been downloaded. Defaults to True.
    """
    if has_downloaded is False:
      print(f'{self.name} - {self.first_season} ({self.data_path})')
      teams_urls = self._get_url_teams(self.url)
      match_history = self._get_team_match_history(self.url, self.first_season, teams_urls)
      if not os.path.exists(self.data_path):
        os.makedirs(self.data_path)
      match_history.to_feather(self.data_path + 'match_history.fea')

    if has_downloaded is True:
      mh_downloaded = pd.read_feather(self.data_path + 'match_history.fea')
      downloaded_seasons = mh_downloaded['season'].unique()
      downloaded_seasons = [season.split('-')[0] for season in downloaded_seasons]
      
      for season in SEASONS_LIST:
        if season not in downloaded_seasons:
          if self.league in ('br'):
            season = season
          else:
            next_year = int(season) + 1
            season = f"{season}-{next_year}"
          url = self.url
          init_season = url.split('/')[6]
          url = url.replace(init_season, season)
          print(f'{self.name} - {season} ({self.data_path})')
          try:
            teams_urls = self._get_url_teams(self.url)
            match_history = self._get_team_match_history(self.url, self.first_season, teams_urls)
            match_history_downloaded = pd.concat([match_history_downloaded, match_history])
            match_history_downloaded.to_feather(self.data_path + 'match_history.fea')
          except Exception as e:
            warnings.warn(f"Error while downloading data for season {season}: {e}")
            continue
        time.sleep(2)
    process_match_history(self.league_code)

  def get_squads(self, has_downloaded= True):
    """Fetch squads players data for the league.

    Parameters:
    -----------
    has_downloaded : bool, optional
        Flag indicating if data has already been downloaded. Defaults to True.
    """
    if has_downloaded is False:
      print(f'{self.name} - {self.first_season} ({self.data_path})')
      teams_urls = self._get_url_teams(self.url)
      squads = provisorio
      #match_history = self._get_team_match_history(self.url, self.first_season, teams_urls)
      if not os.path.exists(self.data_path):
        os.makedirs(self.data_path)
      squads.to_feather(self.data_path + 'squads.fea')

    if has_downloaded is True:
      squads_downloaded = pd.read_feather(self.data_path + 'squads.fea')
      downloaded_seasons = squads_downloaded['season'].unique()
      downloaded_seasons = [season.split('-')[0] for season in downloaded_seasons]
      
      for season in SEASONS_LIST:
        if season not in downloaded_seasons:
          if self.league in ('br'):
            season = season
          else:
            next_year = int(season) + 1
            season = f"{season}-{next_year}"
          url = self.url
          init_season = url.split('/')[6]
          url = url.replace(init_season, season)
          print(f'{self.name} - {season} ({self.data_path})')
          try:
            teams_urls = self._get_url_teams(self.url)
            squads = provisorio
            #match_history = self._get_team_match_history(self.url, self.first_season, teams_urls)
            squads_downloaded = pd.concat([squads_downloaded, squads])
            squads_downloaded.to_feather(self.data_path + 'squads.fea')
          except Exception as e:
            warnings.warn(f"Error while downloading data for season {season}: {e}")
            continue
        time.sleep(2)
    process_squads(self.league_code)