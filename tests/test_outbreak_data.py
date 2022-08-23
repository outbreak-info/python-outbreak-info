import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import requests
import os

from outbreak_data import outbreak_data
test_server = 'test.outbreak.info'
null_server = 'null.outbreak.info'


def _test_network_codes():
    location = 'AUS_SouthAustralia'
    with pytest.raises(requests.ConnectionError):
        out = outbreak_data.get_outbreak_data('covid19/query',
                                              f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,'
                                              f'admin1&{outbreak_data.nopage}', server=null_server, collect_all=True)
        assert isinstance(out, type(None)), f'get_outbreak_data server not returning None despite ConnectionError'


def _test_client_codes():
    location = 'AUS_SouthAustralia'

    with pytest.raises(ValueError):
        out = outbreak_data.get_outbreak_data('covid19/null',
                                              f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,'
                                              f'admin1&{outbreak_data.nopage}', collect_all=True)
        assert isinstance(out, type(None)), f'get_outbreak_data server not returning None despite missing JSON'

    with pytest.raises(ValueError):
        out = outbreak_data.get_outbreak_data('',
                                              f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,'
                                              f'admin1&{outbreak_data.nopage}', collect_all=True)
        assert isinstance(out, type(None)), f'get_outbreak_data server not returning None despite missing JSON'


def test_response_codes():
    _test_network_codes()
    _test_client_codes()


def _test_get_location():
    """
    Test the ability of get data to return a location's case data within a
    pandas dataframe
    """
    location = 'AUS_SouthAustralia'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1'
                                          f'&{outbreak_data.nopage}', server=test_server)
    df = pd.DataFrame(out['hits'])
    assert df.admin1.unique()[0] == 'South Australia', f'get_outbreak_data not returning correct data for {location}'


def _test_get_multiple_locations():
    """
    Test the ability of get data to return multiple locations.
    6/26/2022: Test server so far only supports one location
    """
    location = ['AUS_SouthAustralia', 'USA_US-NY', 'USA_US-TX']
    locations = '(' + ' OR '.join(location) + ')'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{locations}'
                                          f'&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}',
                                          server=test_server)
    df = pd.DataFrame(out['hits'])
    # test server so far only supports one location
    assert len(df.admin1.unique()) == len(location[:1]), f'get_outbreak_data returning incorrect number of locations, ' \
                                                      f'expected {len(location[1:])}'
    location_names = sorted(['South Australia'])
    output_names = sorted(df.admin1.unique())
    for i in range(len(location_names)):
        assert location_names[i] == output_names[i], f'output locations {location_names} do not correspond to input' \
                                                      f' codes: {location}'


def test_get_outbreak_data():
    """
    Main test
    """
    _test_get_location()
    _test_get_multiple_locations()


def _test_cases_single_location():
    location = 'USA_US-CA'
    out = outbreak_data.cases_by_location(location)
    assert out.admin1.unique()[0] == 'California', f'cases_by_location not returning correct data for {location}'


def _test_cases_multiple_location():
    locations = ['USA_US-CA', 'USA_US-NY', 'USA_US-TX']
    out = outbreak_data.cases_by_location(locations)
    assert len(out.admin1.unique()) == len(locations), f'cases_by_location returning an incorrect number of locations,'\
                                                        f' expected {len(locations)}'
    location_names = sorted(['California', 'New York', 'Texas'])
    output_names = sorted(out.admin1.unique())
    for i in range(len(location_names)):
        assert location_names[i] == output_names[i], f'output locations {location_names} do not correspond to input' \
                                                      f' codes: {locations}'


def test_cases_by_location():
    """
    Main test
    """
    _test_cases_single_location()
    _test_cases_multiple_location()
    

class Test_Lineage_Mutations:
    
    def test_one(self): #  Test 1: lineage as string
    
        t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_one.csv'), index_col=0)
        val1 =  outbreak_data.lineage_mutations('BA.2', server=test_server)
        t1 = t1.astype(str)
        val1 = val1.astype(str)
        t1["prevalence"]=t1["prevalence"].values.astype('float')
        val1["prevalence"]=val1["prevalence"].values.astype('float')
        assert assert_frame_equal(t1, val1) is None

    def test_two(self): # Test 2: lineages in list: OR logic
      
        t2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_two.csv'), index_col=0)
        val2 = outbreak_data.lineage_mutations('BA.2 OR B.1.1.7', server=test_server)
        
        t2 = t2.astype(str)
        val2 = val2.astype(str)
        t2["prevalence"]=t2["prevalence"].values.astype('float')
        val2["prevalence"]=val2["prevalence"].values.astype('float')
        assert assert_frame_equal(t2, val2) is None
                
    def test_three(self):  # lineages in list; returning muliple lineages
    
        t3 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_three.csv'), index_col=0)
        val3 = outbreak_data.lineage_mutations('BA.2, B.1.1.7', server=test_server)
        t3 = t3.astype(str)
        val3 = val3.astype(str)
        t3["prevalence"]=t3["prevalence"].values.astype('float')
        val3["prevalence"]=val3["prevalence"].values.astype('float')
        assert assert_frame_equal(t3, val3) is None
    
    
    def test_four(self): # mutation as list: AND logic
    
        t4 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_four.csv'), index_col=0)
        val4 = outbreak_data.lineage_mutations('BA.2','s:p681h', server=test_server)
        t4 = t4.astype(str)
        val4 = val4.astype(str)
        t4["prevalence"]=t4["prevalence"].values.astype('float')
        val4["prevalence"]=val4["prevalence"].values.astype('float')
        assert assert_frame_equal(t4, val4) is None
     
       
def test_lineage_mutations():
    """
    Main test
    """
    Test_Lineage_Mutations().test_one()
    Test_Lineage_Mutations().test_two()
    Test_Lineage_Mutations().test_three()
    Test_Lineage_Mutations().test_four()
    
    
class Test_Prevalence_By_Location:
    
    def test_one(self): # Test 1: Pulls up every lineage on file in USA_US-CO
        t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'prev1.csv'), index_col=0)
        val1 = outbreak_data.prevalence_by_location('USA_US-CO', server=test_server)
        t1 = t1.astype(str)
        val1 = val1.astype(str)
        t1["prevalence"]=t1["prevalence"].values.astype('float')
        val1["prevalence"]=val1["prevalence"].values.astype('float')
        t1["prevalence_rolling"]=t1["prevalence_rolling"].values.astype('float')
        val1["prevalence_rolling"]=val1["prevalence_rolling"].values.astype('float')
        assert assert_frame_equal(t1, val1) is None

    def test_two(self): # Test 2: Pulls up every lineage starting with b.1 on file in USA_US-NY
      
        t2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'prev2.csv'), index_col=0)
        val2 = outbreak_data.prevalence_by_location('USA_US-NY', startswith='b.1', server=test_server)
        
        t2 = t2.astype(str)
        val2 = val2.astype(str)
        t2["prevalence"]=t2["prevalence"].values.astype('float')
        val2["prevalence"]=val2["prevalence"].values.astype('float')
        t2["prevalence_rolling"]=t2["prevalence_rolling"].values.astype('float')
        val2["prevalence_rolling"]=val2["prevalence_rolling"].values.astype('float')
        assert assert_frame_equal(t2, val2) is None
        

def test_prevalence():
    """
    Main test
    """
    Test_Prevalence_By_Location().test_one()
    Test_Prevalence_By_Location().test_two()
