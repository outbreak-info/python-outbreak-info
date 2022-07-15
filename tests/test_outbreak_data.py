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
                                          f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}')
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

def _test_lineage_mutations():
    """
    Main test
    
    Tests:

Ensure that 

1. Passing a single mutation as a string
2. List of mutations
3. Lineage as string
4. List of lineages

    """
    # Make as a Testclass?
    #1 lineage as string
    df = outbreak_data.lineage_mutations('P.1')
    find = list(df['mutation'])
    gamma = ['orf1a:s1188l','orf1a:k1795q', 'orf1a:del3675/3677', 'orf1b:p314l','s:l18f', 's:t20N','s:p26s','s:d138y',
             's:r190s','s:k417t','s:e484k', 's:n501y', 's:d614g',
             's:h655y', 's:t1027i', 's:v1176f','orf3a:s253p','orf8:s84l','orf8:e92k','n:P80r','n:r203k','n:g204r']
    count = 0
    for i in gamma:
        if i not in find:
            count = (count + 1)
            print('Misses:  ' + count) 
        assert i in find
   #checks to see if lineage has gamma mutations
   
   