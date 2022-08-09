from outbreak_tools import outbreak_tools
import pytest
import pandas as pd

def _test_lookup_table():
    output = outbreak_tools.id_lookup([''], table=True)
    assert isinstance(output, pd.core.frame.DataFrame), 'When table is true should return dataframe'

def test_id_lookup():
    _test_lookup_table()