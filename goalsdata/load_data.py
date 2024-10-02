from typing import Literal
import pandas as pd


Regions = Literal["en", "br", "fr", "it", "es", "de"]
Files = Literal["match_history", "standings", "squads"]

def loadData(
    region: Regions, 
    file: Files, 
    raw: bool = False,
) -> pd.DataFrame:
    """
    Loads data for the specified league and file type from the GitHub GOALS-Data repository.

    This function fetches the data from a specified league and file type, either in raw or processed format,
    directly from the GOALS-Data repository on GitHub.

    Parameters
    ----------
    region : Regions
        The code of the league whose data we want to load.
        Allowed values are:
        - 'en' for English Premier League
        - 'br' for Brasileirão (Brazilian League)
        - 'fr' for Ligue 1 (French League)
        - 'it' for Serie A (Italian League)
        - 'es' for La Liga (Spanish League)
        - 'de' for Bundesliga (German League)
    file : Files
        The type of file to be loaded.
        Allowed values are:
        - 'match_history' for match history data
        - 'standings' for league standings data
        - 'squads' for team squads data
    raw : bool, optional
        If True, loads raw data ('raw_data'). Otherwise, loads processed data ('processed_data').
        Default value is False.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data loaded from the CSV file.

    Raises
    ------
    ValueError
        If the provided `region` or `file` is not valid.
        If there is an issue loading the CSV file from the URL.
    
    Examples
    --------
    Load processed match history data for the Brasileirão:

    >>> df = loadData('br', 'match_history')
    >>> print(df.head())

    Load raw standings data for the Premier League:

    >>> df = loadData('en', 'standings', raw=True)
    >>> print(df.head())
    """
    data_type = 'raw_data' if raw else 'processed_data'
    
    valid_region = {
        'en': 'premier_league', 
        'br': 'brasileirao', 
        'fr': 'league_1', 
        'it': 'serie_a',
        'es': 'la_liga', 
        'de': 'bundesliga'
    }

    if region not in valid_region:
        raise ValueError(f"Invalid value for 'region': {region}. Allowed values: {list(valid_region.keys())}")

    league = valid_region[region]

    url = f"https://raw.githubusercontent.com/salvnetto/GOALS-Data/main/datasets/{data_type}/{league}/{file}.csv"

    try:
        data = pd.read_csv(url)
    except Exception as e:
        raise ValueError(f"Error while importing data from {url}: {e}")
    
    return data
