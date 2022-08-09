from outbreak_tools import outbreak_tools
import pytest
import pandas as pd

def _test_lookup_table():
    output = outbreak_tools.id_lookup([''], table=True)
    assert isinstance(output, pd.core.frame.DataFrame), 'When table is true should return dataframe'

def _test_single_location():
    location = 'USA_US-CA'
    plot = outbreak_tools.plot_case_increase(location)

    assert(type(plot) == alt.vegalite.v4.api.Chart)

def test_plot_increase():
    """
    Tests the cases_by_location visualization tool in outbreak_tools
    """
    _test_single_location()

def test_id_lookup():
    _test_lookup_table()
