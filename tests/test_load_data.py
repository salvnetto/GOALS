import pytest
import pandas as pd

from goals import loadData


def testLoadDataValidInput():
    # Test valid input
    df = loadData('br', 'match_history')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def testLoadDataInvalidRegion():
    # Test invalid region
    with pytest.raises(ValueError):
        loadData('invalid_region', 'match_history')

def testLoadDataInvalidFile():
    # Test invalid file
    with pytest.raises(ValueError):
        loadData('br', 'invalid_file')

def testLoadDataInvalidUrl():
    # Test invalid URL (simulate URL not found)
    with pytest.raises(ValueError):
        loadData('br', 'match_history', raw=True)

