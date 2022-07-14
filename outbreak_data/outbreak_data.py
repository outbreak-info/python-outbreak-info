import requests
import pandas as pd
import re

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def get_outbreak_data(endpoint, argstring, server=server, auth=auth,  collect_all=False):
    """
    Receives raw data using outbreak API.

    :param endpoint: directory in server the data is stored
    :param argstring: feature arguments to provide to API call
    :param server: Server to request from
    :param auth: Auth key
    :param collect_all: if True, returns all data.
    :return: A request object containing the raw data
    """
    def format_data(data):
        data['date'] = data['date'].apply(lambda x: pd.to_datetime(x))
        data = data.sort_values(by='date', ascending=True)
        data.reset_index(drop=True, inplace=True)
        return data
    auth = {'Authorization': str(auth)}
    # initial request // used to collect data during recursion or as output of single API call
    in_req = requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth)
    valid_req = 'success' not in in_req.json().keys()
    if collect_all is False:
        try:
            in_data = pd.DataFrame(in_req.json()['results'])
            return format_data(in_data)
        except KeyError:
            print("Request not returning any data with 'results' keyword")
            try:
                in_data = pd.DataFrame(in_req.json()['hits'])
                return format_data(in_data)
            except KeyError:
                print("Request not returning any data with 'hits' keyword")
                pass
    elif collect_all and not valid_req:
        return
    elif collect_all and valid_req:
        # initial pandas dataframe set and updating page for collecting new data
        in_data = pd.DataFrame(in_req.json()['hits'])
        # base case check for ending recursion
        scroll_id = in_req.json()['_scroll_id']
        fetching_page = '&fetch_all=True&page='
        next_page = int(re.search(r'(?<=page=)\d+', argstring).group(0)) + 1
        page = fetching_page + str(next_page)
        to_scroll = 'scroll_id=' + scroll_id + page
        in_data = in_data.append(get_outbreak_data(endpoint, to_scroll, collect_all=True))
        return format_data(in_data)

# minimal working version
# def cases_by_location(location, server=server, auth=auth):
#     """
#     Loads data from a location; Use 'OR' between locations to get multiple.
#     Since this API endpoint supports paging, collect_all is used to return all data.
#     :param location: A string
#     :return: A pandas dataframe
#     """
#     args = f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}'
#     return get_outbreak_data(covid19_endpoint, args, collect_all=True)

# Hritika's smoothed-data version (WIP)
#def cases_by_location(location, server=server, auth=auth, pull_smoothed=0):
#    """
#    Loads data from a location; Use 'OR' between locations to get multiple.
#    Arguments:
#        location: A string
#    Returns:
#        A pandas dataframe
#    """
#    raw_data = get_outbreak_data(covid19_endpoint,
#                                                 f'location_id:{location}&sort=date&fields=date,{confirmed},admin1&{nopage}',
#                                                 server, auth)
#    print_raw=raw_data.json()['hits']
#    print_raw_table=pd.DataFrame(print_raw)
#    refined_table=print_raw_table.drop(columns=['_score', 'admin1'], axis=1)
#    if pull_smoothed == 0:
#        confirmed='confirmed_numIncrease'
#        print(refined_table)
#    elif pull_smoothed == 1:
#        confirmed='confirmed_rolling'
#        print(refined_table)
#    elif pull_smoothed == 2:
#        confirmed='confirmed_rolling','confirmed_numIncrease'
#        print(refined_table)
#    else:
#        print("invalid parameter value!")

# Sarah's multiple-locations version (WIP)
def cases_by_location(location, server=server, auth=auth):
    """
    Loads data from a location if input is a string, or from multiple locations
    if location is a list of string locations.
    Since this API endpoint supports paging, collect_all is used to return all data.
    :param location: A string or list of strings
    :return: A pandas dataframe
    """
    # location names can be further checked to verify validity // proper format
    if isinstance(location, str):  # Converts all location input strings into lists: best universal input 
      location = location.replace(" ", "")
      location = list(location.split(","))     
    if not isinstance(location, list) or len(location) == 0:
        raise ValueError('Please enter at least 1 valid location id')
    try:
        locations = '(' + ' OR '.join(location) + ')'
        args = f'q=location_id:{locations}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}'
        df = get_outbreak_data(covid19_endpoint, args, collect_all=True) 
        for i in location:  # checks each entry in location for invalid location ids after request
                check = i[0:2] #checks for first 3 letters from string input in df; if they're there, the df passed
                valid_loc = df.loc[df['_id'].str.startswith(check)]
                if valid_loc.empty:
                    print('{} is not a valid location ID'.format(i))
        if not df.empty:
            return df
    except:
        for i in location:
            print('{} is not a valid location ID'.format(i))
            
            
            
def get_outbreak_data_no_paging(endpoint, argstring, server=server, auth=auth):
    
    """Works similarly to get_outbreak_data. Used for API enpoints
       that do not support paging
    
    Arguments: 
        endpoint: directory in server the data is stored
        argstring: feature arguments to provide to API call
    
    Returns: 
        A request object containing the raw data"""
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth) 


def prevalence_by_location(location, startswith=None, server=server, auth=auth):

    lins = get_outbreak_data('genomics/prevalence-by-location-all-lineages',
                                          f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0')
    
    """Loads prevalence data from a location
            Arguments:
                :param location: A string
                :param num_pages: For every value >= 0, returns 1000 obs. (paging)
                :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
            Returns:
                A pandas dataframe"""

    if startswith is not None:
       return lins.loc[lins['lineage'].str.startswith(startswith)]
    return lins
  
    
def lineage_mutations(pango_lin, mutation=None, freq=0.8, server=server, auth=auth):
    
    """Retrieves data from all mutations in a specified lineage above a frequency threshold
       Mutiple queries for lineages and mutations can be separated by ','
    
          Arguments:
             :param pango_lin: A string or list; loads data for all mutations in a specified PANGO lineage 
             :param mutation: A string or list; loads data for lineages containing a specified mutation
             :param freq: a number between 0 and 1 specifying the frequency threshold above which to return mutations (default = 0.8)
          Returns:
              A pandas dataframe"""
              
    # Turns any string input into list format: most universal
    
    if type(pango_lin) == str:
         pango_lin = pango_lin.replace(" ", "")
         pango_lin = list(pango_lin.split(","))
    if mutation is not None and type(mutation) == str:
          mutation = mutation.replace(" ", "")
          mutation = list(mutation.split(","))
    if isinstance(pango_lin, list):
       pass
    if mutation is not None and isinstance(mutation, list):
       pass
    if mutation is None:
        lineages = '' + ' OR '.join(pango_lin) 
    else:
        lineages = '' + ' OR '.join(pango_lin) + ' AND ' + ' AND '.join(mutation) + '' 
    raw_data = get_outbreak_data_no_paging('genomics/lineage-mutations', f'pangolin_lineage={lineages}').json()['results']
    df = pd.DataFrame(raw_data[lineages]) 
          
    if freq != 0.8:
        if isinstance(freq, float) and freq > 0 and freq < 1:
          return df.loc[df['prevalence'] >= freq]
    else:
        return df

