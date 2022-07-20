import pytest
# Used the request the data from the API
import requests
# Used to parse the datetime features in the data
from datetime import datetime
# Used to write the urls to call the API with
from urllib.parse import urljoin
# Used to introduce delays between tests to avoid overloading the API.
from time import sleep, time
import sys
sys.path.append('/Users/sarahrandall/Python-outbreak-info/outbreak_data')
from outbreak_data import outbreak_data


# def _test_get_location():
#     """
#     Test the ability of get data to return a location's case data within a
#     pandas dataframe
#     """
#     location = 'USA_US-CA'
#     out = outbreak_data.get_outbreak_data('covid19/query',
#                             f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}')
#     assert(out.admin1.unique()[0] == 'California')


# def _test_get_multiple_locations():
#     """
#     Test the ability of get data to return multiple locations.
#     """
#     location = '(USA_US-CA OR USA_US-NY)'
#     out = outbreak_data.get_outbreak_data('covid19/query',
#                                           f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}')
#     assert(len(out.admin1.unique()) == 2)


# def _test_page_data():
#     pass


# def test_get_outbreak_data():
#     """
#     Main test
#     """
#     _test_get_location()
#     _test_get_multiple_locations()


# def test_cases_by_location():
#     """
#     Main test
#     """
#     pass

class Test_Lineage_Mutations:
    
    gamma = ['orf1a:s1188l','orf1a:k1795q', 'orf1a:del3675/3677', 'orf1b:p314l','orf1b:e1264d', 's:l18f', 's:t20n','s:p26s','s:d138y',
               's:r190s','s:k417t','s:e484k', 's:n501y', 's:d614g',
               's:h655y', 's:t1027i', 's:v1176f','orf3a:s253p','orf8:s84l','orf8:e92k','n:p80r','n:r203k','n:g204r']

    alpha = ['orf1a:t1001i','orf1a:a1708d', 'orf1a:i2230t', 'orf1a:del3675/3677', 'orf1b:p314l','s:del69/70', 's:del144/144','s:n501y','s:a570d',
            's:r190s','s:k417t','s:e484k', 's:n501y', 's:d614g',
            's:d614g', 's:p681h', 's:t716i','s:s982a','s:d1118h','orf8:q27*','orf8:r52i','orf8:y73c','orf8:s84l', 
            'n:d3l', 'n:r203k','n:g204r', 'n:s235f']   
    
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

    def test_two(self): # Test 2: lineages in list 
    
        """AND logic is typically intersection, "OR" logic refer to something that's in one or the other - it could be an overlapping mutation or it could be unique.
        Use OR for lineages and "AND" for mutations that get passed
        For example, if  mutation "mut_A" occurs in lineage "A" but not in lineage "B", and you query for lineage "A", OR lineage "B", 
        then "mut_A" should always be returned. 
        If "mut_A" happens to overlap in lineage "A" and lineage "B", "mut_A" should still be returned. 
        Evaluates each query/condition for "is this mutation in this lineage?" separately then combines.
        """
        # test each lineage seperately then test if combined result matches
        df1 = outbreak_data.lineage_mutations('P.1') # gamma
        find1 = list(df1['mutation'])

        df2 = outbreak_data.lineage_mutations('B.1.1.7') # alpha
        find2 = list(df2['mutation'])
        # Note: df1, df2, find1 and find2 not required for this test to run smoothly

        df3 = outbreak_data.lineage_mutations('P.1, B.1.1.7') # gamma or alpha logic test
        find3 = list(df3['mutation'])

        f1 = [] #unique to gamma
        f2 = [] # unique to alpha
        shared = [] # shared mutations

        # Finds unique mutations in each variant
        for i in find3:
              if i in find1 and i in find2:
                  shared.append(i)
              elif i in find1:
                      f1.append(i)
              elif i in find2:
                      f2.append(i)
                     
        # df3 dataframe includes all mutations alpha and gamma have in common including alpha's unique lineages 
        # there are no mutations unique to gamma since they would be found in both[]

        if len(shared) == 0: 
            assert find3.empty  # this line most likely will never run, as lineage_mutations will catch this now
            
        for i in shared:
            assert i in find3
            
        if len(f1) != 0:
            for i in f1:
                  assert i in find3

        if len(f2) != 0:
            for i in f2:
                assert i in find3
                
    # def test_three(self):
    #     pass
        

     
   
   