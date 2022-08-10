import sys
sys.path.insert(0, '/Users/sarahrandall/Python-outbreak-info/outbreak_data') 
sys.path.insert(0, '/Users/sarahrandall/Python-outbreak-info/outbreak_tools')
import pandas as pd
import outbreak_data
import requests
server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'

def get_prevalence_by_location(endpoint, argstring, server=server, auth=auth):
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth) 
 
def prevalence_by_location(location, pango_lin = None, startswith=None, server=server, auth=auth):
       """
       Loads prevalence data from a location

       Arguments:
           :param location: A string
           :param num_pages: For every value >= 0, returns 1000 obs. (paging)
           :param pango_lin: A string; loads data for a specifc lineage
           :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
       Returns:
           A pandas dataframe
       """
       raw_data = outbreak_data.get_prevalence_by_location('genomics/prevalence-by-location-all-lineages', f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0').json()['results']
       lins = pd.DataFrame(raw_data)
        
       if startswith is not None:
          search_all = startswith
          return lins.loc[lins['lineage'].str.startswith(search_all)]
       else:
          return lins.loc[lins['lineage']== pango_lin]
      
if __name__ == "__main__":                                                                                                   
   foo = prevalence_by_location('USA','b.1.1.2')
   print('Hello World')
   print(foo)
