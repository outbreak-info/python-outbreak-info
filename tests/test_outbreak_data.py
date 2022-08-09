import pandas as pd
import pytest
import requests

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
    
   val1 = pd.read_csv('')
    
    def test_one(self): #  Test 1: lineage as string
        
      df = outbreak_data.lineage_mutations('P.1') # P.1 contains all gamma mutations
      find = list(df['mutation'])
      g_miss_count = 0 
      for i in find:
          if i in self.gamma:
               pass
          else:
              g_miss_count +=1
      a_miss_count = 0 
      for i in find:
          if i in self.alpha:
                pass
          else:
             a_miss_count +=1

      assert g_miss_count == 0    
      assert a_miss_count > 0

    def test_two(self): # Test 2: lineages in list: OR logic
    
        """AND logic is typically intersection, "OR" logic refer to something that's in one or the other - it could be an overlapping mutation or it could be unique.
        Use OR for lineages and "AND" for mutations that get passed
        For example, if  mutation "mut_A" occurs in lineage "A" but not in lineage "B", and you query for lineage "A", OR lineage "B", 
        then "mut_A" should always be returned. 
        If "mut_A" happens to overlap in lineage "A" and lineage "B", "mut_A" should still be returned. 
        Evaluates each query/condition for "is this mutation in this lineage?" separately then combines.
        """
        # test each lineage seperately then test if combined result matches
        df1 = outbreak_data.lineage_mutations('BA.2') # BA.2
        find1 = list(df1['mutation'])
        df2 = outbreak_data.lineage_mutations('B.1.1.7') # B.1.1.7
        find2 = list(df2['mutation'])
        
        args = ['BA.2 OR B.1.1.7']
        df3 = outbreak_data.lineage_mutations(args) # BA.2 or B.1.1.7 logic test
        find3 = list(df3['mutation'])
        shared = [] # shared mutations
        # Finds unique mutations in each variant
        for i in find3:
              if i in find1 and i in find2:
                  shared.append(i)
              elif i in find1:
                      self.f1.append(i)
              elif i in find2:
                      self.f2.append(i)
                     
        # df3 dataframe includes all mutations both lineages have in common
        if len(shared) == 0: 
            assert find3.empty  # this line most likely will never run, as lineage_mutations will catch this now
        for i in shared:
            assert i in find3
                
    def test_three(self):  # lineages in list; returning muliple lineages
        t1 = outbreak_data.lineage_mutations('BA.2')
        find1 = list(t1['mutation'])
        t2 = outbreak_data.lineage_mutations('B.1.1.7')
        find2 = list(t2['mutation'])
        t3 = outbreak_data.lineage_mutations(['BA.2','B.1.1.7'])
        find3 = list(t3['mutation'])
        size = len(find1) + len(find2)
        assert len(find3) == size
    
    def test_four(self): # mutation as list: AND logic
     
    # Part 1: P.1 with S:P681H
        """Return mutations for sequences classified as P.1 with S:P681H mutation
           Lineage counts will match outbreak.info's data if true"""
           
        mutation =  ['s:p681h']
        try1 = outbreak_data.lineage_mutations('P.1', mutation)
        find1 = list(try1['mutation']) 
        lin_count = list(try1['lineage_count'])

        for i in mutation:
            assert i in find1
        for i in lin_count:
            assert i == 287 #According to outbreak.info
       
    # Part 2: 2 lineages: orf1a:i2230t and s:p681h
        """Return mutations for sequences classified as P.1 with S:P681H AND orf1a:i2230t mutations"""
        mutation = ['orf1a:i2230t', 's:p681h']
        try2 = outbreak_data.lineage_mutations('P.1', mutation)
        find1 = list(try2['mutation']) 
        lin_count = list(try2['lineage_count'])  #outbreak.info says there are 3 sequences that fall under this category
       
        for i in mutation:
            assert i in find1
        for i in lin_count:
            assert i == 3
           
     # Part 3: Fails appropriately
        mutations = ['orf1a:t1001i', 's:t716i', 'orf8:y73c'] 
        try:
              try3 = outbreak_data.lineage_mutations('P.1', mutations) # this should not work
        except:
              invalid = True
              
        assert(invalid)

