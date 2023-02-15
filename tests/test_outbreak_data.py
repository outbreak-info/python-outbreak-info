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
        t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'test_one.csv'), index_col=0)
        val1 =  outbreak_data.lineage_mutations('BA.2', server=test_server)
        t1 = t1.astype(str)
        val1 = val1.astype(str)
        t1["prevalence"]=t1["prevalence"].values.astype('float')
        val1["prevalence"]=val1["prevalence"].values.astype('float')
        assert_frame_equal(t1, val1)

    def test_two(self): # Test 2: lineages in list: OR logic
      
        t2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'test_two.csv'), index_col=0)
        val2 = outbreak_data.lineage_mutations('BA.2 OR B.1.1.7', server=test_server)
        
        t2 = t2.astype(str)
        val2 = val2.astype(str)
        t2["prevalence"]=t2["prevalence"].values.astype('float')
        val2["prevalence"]=val2["prevalence"].values.astype('float')
        assert_frame_equal(t2, val2)
                
    def test_three(self):  # lineages in list; returning muliple lineages
    
        t3 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'test_three.csv'), index_col=0)
        val3 = outbreak_data.lineage_mutations('BA.2, B.1.1.7', server=test_server)
        t3 = t3.astype(str)
        val3 = val3.astype(str)
        t3["prevalence"]=t3["prevalence"].values.astype('float')
        val3["prevalence"]=val3["prevalence"].values.astype('float')
        assert_frame_equal(t3, val3)
    
    
    def test_four(self): # mutation as list: AND logic
    
        t4 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'test_four.csv'), index_col=0)
        val4 = outbreak_data.lineage_mutations('BA.2','s:p681h', server=test_server)
        t4 = t4.astype(str)
        val4 = val4.astype(str)
        t4["prevalence"]=t4["prevalence"].values.astype('float')
        val4["prevalence"]=val4["prevalence"].values.astype('float')
        assert_frame_equal(t4, val4)
     
       
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
        t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'prev1.csv'), index_col=0)
        val1 = outbreak_data.prevalence_by_location('USA_US-CO', server=test_server)
        t1 = t1.astype(str)
        val1 = val1.astype(str)
        t1["prevalence"]=t1["prevalence"].values.astype('float')
        val1["prevalence"]=val1["prevalence"].values.astype('float')
        t1["prevalence_rolling"]=t1["prevalence_rolling"].values.astype('float')
        val1["prevalence_rolling"]=val1["prevalence_rolling"].values.astype('float')
        assert_frame_equal(t1, val1)

    def test_two(self): # Test 2: Pulls up every lineage starting with b.1 on file in USA_US-NY
      
        t2 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'prev2.csv'), index_col=0)
        val2 = outbreak_data.prevalence_by_location('USA_US-NY', startswith='b.1', server=test_server)
        t2 = t2.astype(str)
        val2 = val2.astype(str)
        t2["prevalence"]=t2["prevalence"].values.astype('float')
        val2["prevalence"]=val2["prevalence"].values.astype('float')
        t2["prevalence_rolling"]=t2["prevalence_rolling"].values.astype('float')
        val2["prevalence_rolling"]=val2["prevalence_rolling"].values.astype('float')
        assert_frame_equal(t2, val2)
        

def test_prevalence():
    """
    Main test
    """
    Test_Prevalence_By_Location().test_one()
    Test_Prevalence_By_Location().test_two()
    
    

class Test_Sequence_Counts:
    
    def test_one(self):
        t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count1.csv'), index_col=0)
        val1 = outbreak_data.sequence_counts(server=test_server)
        t1 = t1.astype(str)
        val1 = val1.astype(str)
        assert_frame_equal(t1, val1)
        
    def test_two(self):
        t2 = pd.read_csv(os.path.join(os.path.dirname(__file__),'test_data', 'seq_count2.csv'), index_col=0)
        val2 = outbreak_data.sequence_counts('USA_US-CA', server=test_server)
        t2 = t2.astype(str)
        val2 = val2.astype(str)
        assert_frame_equal(t2, val2)
    
    def test_three(self):
        t3 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count3.csv'), index_col=0)
        val3 = outbreak_data.sequence_counts('USA', cumulative=True, server=test_server)
        t3 = t3.astype(str)
        val3 = val3.astype(str)
        assert_frame_equal(t3, val3)
        
    def test_four(self):
        t4 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count4.csv'), index_col=0)
        val4 = outbreak_data.sequence_counts('USA', True, True, server=test_server)
        t4 = t4.astype(str)
        val4 = val4.astype(str)
        assert_frame_equal(t4, val4)

def test_seq_counts():
    """
    Main test
    """
    Test_Sequence_Counts().test_one()
    Test_Sequence_Counts().test_two()
    Test_Sequence_Counts().test_three()
    Test_Sequence_Counts().test_four()
    
    
def _test_global_prevalence():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'global_prev_test.csv'), index_col=0)
    val1 = outbreak_data.global_prevalence('ba.2', 'orf1a:t842i', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    t1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=t1[["total_count_rolling", "lineage_count_rolling","proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    val1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=val1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    assert_frame_equal(t1, val1)
    
def test_global_prevalence():
    """
    Main test
    """
    _test_global_prevalence()
    
def _mutations_by_lineage():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'mut_across_lin_test.csv'), index_col=0)
    val1 = outbreak_data.mutations_by_lineage('orf1a:g1307s', 'USA', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    t1[[ "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=t1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    val1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=val1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    assert_frame_equal(t1, val1)
        
def mutations_by_lineage():
    """
    Main test
    """
    _mutations_by_lineage()
    
def _test_daily_prev():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'daily_prev.csv'), index_col=0)
    val1 = outbreak_data.daily_prev('BA.2', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    t1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=t1[["total_count_rolling", "lineage_count_rolling","proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    val1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=val1[["total_count_rolling", "lineage_count_rolling", "proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    assert_frame_equal(t1, val1)

def test_daily_prev():
    """
    Main test
    """
    _test_daily_prev()

def _test_lineage_by_sub_admin():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'sub_admin.csv'), index_col=0)
    t1 = t1.dropna(axis = 0)
    val1 = outbreak_data.lineage_by_sub_admin('XBB.1.5', location='USA', server=test_server)
    val1 = val1.drop(0)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    t1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=t1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    val1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]]=val1[["proportion", 'proportion_ci_lower', 'proportion_ci_upper' ]].values.astype('float')
    assert_frame_equal(t1, val1)


def test_lineage_by_sub_admin():
    """
    Main test
    """
    _test_lineage_by_sub_admin()

def _test_collection_date():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'collection_date.csv'), index_col=0)
    val1 = outbreak_data.collection_date('BA.1', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)

def test_collection_date():
    """
    Main test
    """
    _test_collection_date()

def _test_submission_date():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'submission_date.csv'), index_col=0)
    val1 = outbreak_data.submission_date('BA.1', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)

def test_submission_date():
    """
    Main test
    """
    _test_submission_date()

def _test_mutation_details():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'mutation_details.csv'), index_col=0)
    val1 = outbreak_data.mutation_details('orf1a:t842i', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)

def test_mutation_details():
    """
    Main test
    """
    _test_mutation_details()

def _test_daily_lag():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'daily_lag.csv'), index_col=0)
    val1 = outbreak_data.daily_lag('LUX', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)

def test_daily_lag():
    """
    Main test
    """
    _test_daily_lag()
    
    
def _test_wildcard_lineage():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_lineage.csv'), index_col=0)
    val1 = wildcard_lineage('b.1*', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)

def test_wildcard_lineage():
    """
    Main test
    """
    _test_wildcard_lineage()

def _test_wildcard_location():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_location.csv'), index_col=0)
    val1 = wildcard_location('united*', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)


def test_wildcard_location():
    """
    Main test
    """
    _test_wildcard_location()

def _test_location_details():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'location_details.csv'), index_col=0)
    val1 = location_details('CHN', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)


def test_location_details():
    """
    Main test
    """
    _test_location_details()
    

def _test_wildcard_mutations():
    t1 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_mutations.csv'), index_col=0)
    val1 = wildcard_mutations('s:e484*', server=test_server)
    t1 = t1.astype(str)
    val1 = val1.astype(str)
    assert_frame_equal(t1, val1)


def test_wildcard_mutations():
    """
    Main test
    """
    _test_wildcard_mutations()



































    
