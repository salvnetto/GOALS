# GOALS - Game Outcome Analysis using Learning Statistics

## Overview

The `GOALS` package facilitates game outcome analysis using statistical learning techniques. It is designed for modeling and predicting football match results based on various statistical features.

## Features

- Web scraping techniques to gather football data.
- Preprocessing functions for cleaning and transforming data.

## Usage

To use the `GOALS` package, install it via pip:

```
pip install GOALS-Football
```

### Example: Loading Data

```python
from goalsdata import loadData

# Load processed match history data for Brasileirão
df = loadData('br', 'match_history')
print(df.head())

# Load raw standings data for the Premier League
df = loadData('en', 'standings', raw=True)
print(df.head())
```