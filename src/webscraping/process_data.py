import os
import pandas as pd

def save_path(file, file_name, league):
  processed_path = f'../datasets/processed_data/{league}/'
  if not os.path.exists(processed_path):
    os.makedirs(processed_path)
  file.to_feather(processed_path + f'{file_name}.fea')


def process_standing(league):
  standing = pd.read_feather(f'../datasets/raw_data/{league}/standing.fea')
  standing.columns = standing.columns.str.lower()
  standing = standing.drop(
    ['pts/mp', 'top team scorer', 'goalkeeper', 'notes'], 
    axis= 1)
  save_path(standing, 'standing', league)
  
def process_match_history(league):
  match_history = pd.read_feather(f'../datasets/raw_data/{league}/match_history.fea')
  match_history.columns = match_history.columns.str.lower()
  match_history = match_history.drop(
    ['match report', 'time', 'day'],
    axis= 1)
  save_path(match_history, 'match_history', league)
