import requests
import pandas as pd

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def get_outbreak_data(endpoint, argstring, server=server, auth=auth,  collect_all=False, curr_page=0):
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
    valid_req = 'success' not in in_req.json().keys()
    # initial pandas dataframe set and updating page for collecting new data
    if valid_req:
        in_data = pd.DataFrame(in_req.json()['hits'])
        # applying datetime to dates column and sorting in ascending
        in_data['date'] = in_data['date'].apply(lambda x: pd.to_datetime(x))
        if collect_all:
            # base case check for ending recursion
            scroll_id = in_req.json()['_scroll_id']
            fetching_page = '&fetch_all=True&page='
            page = fetching_page + str(curr_page)
            to_scroll = 'scroll_id=' + scroll_id + page
            in_data = in_data.append(get_outbreak_data(endpoint, to_scroll, collect_all=True, curr_page=curr_page+1))
        in_data = in_data.sort_values(by='date', ascending=True)
        in_data.reset_index(drop=True, inplace=True)
        return in_data
    return

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
    
    # Converts all location input strings into lists: best universal input 
    
    if type(location) == str:
      
      location = location.replace(" ", "")
      location = list(location.split(","))     
      assert(type(location == list))
      
    try:
        locations = '(' + ' OR '.join(location) + ')'
        args = f'q=location_id:{locations}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}'
        df = get_outbreak_data(covid19_endpoint, args, collect_all=True) # only one request!
        
        for i in location:  # checks each entry in location for invalid location ids after request
                valid_loc = df.loc[df['_id'].str.startswith(i)]
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
    
    raw_data = get_outbreak_data_no_paging('genomics/prevalence-by-location-all-lineages', 
                                          f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0').json()['results']
    lins = pd.DataFrame(raw_data)
    
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
  
    