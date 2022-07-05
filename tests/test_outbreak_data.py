import pytest
# Used the request the data from the API
import requests
# Used to parse the datetime features in the data
from datetime import datetime
# Used to write the urls to call the API with
from urllib.parse import urljoin
# Used to introduce delays between tests to avoid overloading the API.
from time import sleep, time
from outbreak_data import outbreak_data


def _test_get_location():
    """
    Test the ability of get data to return a location's case data within a
    pandas dataframe
    """
    location = 'USA_US-CA'
    out = outbreak_data.get_outbreak_data('covid19/query',
                            f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}')
    assert(out.admin1.unique()[0] == 'California')


def _test_get_multiple_locations():
    """
    Test the ability of get data to return multiple locations.
    """
    location = '(USA_US-CA OR USA_US-NY)'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}')
    assert(len(out.admin1.unique()) == 2)


def _test_page_data():
    pass


def test_get_outbreak_data():
    """
    Main test
    """
    _test_get_location()
    _test_get_multiple_locations()


def test_cases_by_location():
    """
    Main test
    """
    pass
