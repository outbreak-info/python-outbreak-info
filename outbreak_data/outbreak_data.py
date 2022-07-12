import requests
import pandas as pd

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def get_outbreak_data(endpoint, argstring, server=server, auth=auth,  collect_all=False, in_data=None, curr_page=None):
    """
    Receives raw data using outbreak API.
    Must append 'q=' to argstring if initiating non-scrolling query (default).

    :param endpoint: directory in server the data is stored
    :param argstring: feature arguments to provide to API call
    :param server: Server to request from
    :param auth: Auth key
    :param collect_all: if True, returns all data.
    :param in_data: Parent data during recursion.
    :param curr_page: Page to access during next step of recursion.
    :return: A request object containing the raw data
    """
    auth = {'Authorization': str(auth)}
    # initial request // used to collect data during recursion or as output of single API call
    in_req = requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth)
    # initial pandas dataframe set and updating page for collecting new data
    if in_data is None:
        # initial df
        in_data = pd.DataFrame(in_req.json()['hits'])
    # base case check for returning data w/wo recursion
    if collect_all:
        # recursion state
        if 'success' not in in_req.json().keys():
            if curr_page is not None:
                data = pd.DataFrame(in_req.json()['hits'])
                out_data = in_data.append(data, ignore_index=True)
            else:
                out_data = in_data
                curr_page = 0
            scroll_id = in_req.json()['_scroll_id']
            fetching_page = '&fetch_all=True&page='
            page = fetching_page + str(curr_page)
            to_scroll = 'scroll_id=' + scroll_id + page
            return get_outbreak_data(endpoint, to_scroll, collect_all=True, in_data=out_data, curr_page=curr_page+1)

    # non-recursion state
    # applying datetime to dates column and sorting in ascending
    in_data['date'] = in_data['date'].apply(lambda x: pd.to_datetime(x))
    in_data = in_data.sort_values(by='date', ascending=True)
    in_data.reset_index(drop=True, inplace=True)
    return in_data


def cases_by_location(location, server=server, auth=auth):
    """
    Loads data from a location if input is a string, or from multiple locations
    if location is a list of string locations.
    Since this API endpoint supports paging, collect_all is used to return all data.

    :param location: A string or list of strings
    :return: A pandas dataframe

    """
    # location names can be further checked to verify validity // proper format
    
    if type(location) == list:
        for i in location:
            try:
                locations = '(' + ' OR '.join(location) + ')'
                bad_input = ('{} is not a valid location ID'.format(i))
                args = f'q=location_id:{locations}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}'
                df = get_outbreak_data(covid19_endpoint, args, collect_all=True)
                if not df.empty:
                    return df
            except:
                print(bad_input)
            
    else:
        bad_input = ('{} is not a valid location ID'.format(location))
        try:
            bad_input = ('{} is not a valid location ID'.format(location))
            args = f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}'
            df = get_outbreak_data(covid19_endpoint, args, collect_all=True)
            if not df.empty:
                return df
        except:
            print(bad_input)
            
            
def get_prevalence_by_location(endpoint, argstring, server=server, auth=auth):
    
    """Used with prevalence_by_location. Works similarly to get_outbreak_data. 
        Prevalence_by_location() does not support paging.
    
    Arguments: 
        endpoint: directory in server the data is stored
        argstring: feature arguments to provide to API call
    
    Returns: 
        A request object containing the raw data"""
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth) 


def prevalence_by_location(location, pango_lin = None, startswith=None, server=server, auth=auth):
    raw_data = get_prevalence_by_location('genomics/prevalence-by-location-all-lineages', f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0').json()['results']
    lins = pd.DataFrame(raw_data)
    
    """Loads prevalence data from a location

            Arguments:
                :param location: A string
                :param pango_lin: A string; loads data for a specifc lineage
                :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
            Returns:
                A pandas dataframe"""
               
    if startswith is not None:
        search_all = startswith
        return lins.loc[lins['lineage'].str.startswith(search_all)]
    else:
        return lins.loc[lins['lineage']== pango_lin]
    
    
    
def lineage_mutations(pango_lin, mutation=None, freq=None, server=server, auth=auth):
    
    # Turns any string input into list format: most universal
    
      if type(pango_lin) == str:
          
         pango_lin = pango_lin.replace(" ", "")
      
         pango_lin = list(pango_lin.split(","))
       
      
      if mutation is not None and type(mutation) == str:
          
          mutation = mutation.replace(" ", "")
          
          mutation = list(mutation.split(","))
         
      assert(type(pango_lin == list))
      assert(type(mutation == list)) 
      
      
      if mutation is None:
          lineages = '' + ' OR '.join(pango_lin) 
      
      else:
          lineages = '' + ' OR '.join(pango_lin) + ' AND ' + ' AND '.join(mutation) + '' #not concatenating correctly or not the right query?
            
      raw_data = get_prevalence_by_location('genomics/lineage-mutations', f'pangolin_lineage={lineages}').json()['results']
            
      df = pd.DataFrame(raw_data[lineages]) # see how to access list values in a dictionary
            
      if freq is not None:
          assert(type(freq == float))
          return df.loc[df['prevalence'] >= freq]
      
      return df
          
         