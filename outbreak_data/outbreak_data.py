import pandas as pd
import requests

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = ***REMOVED***  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'
lineage_endpoint = 'genomics/lineage-mutations'
prevalence_endpoint = 'genomics/prevalence-by-location-all-lineages'
valid_servers = [server, 'dev.outbreak.info', 'test.outbreak.info']


def get_outbreak_data(endpoint, argstring, server_url=None, auth_key=auth, collect_all=False, curr_page=0):
    """
    Receives raw data using outbreak API.

    :param endpoint: directory in server the data is stored
    :param argstring: feature arguments to provide to API call
    :param server_url: Server to request from
    :param auth_key: Auth key (defaults to acceptable state)
    :param collect_all: if True, returns all data.
    :param curr_page: iterator state for paging
    :return: A request object containing the raw data
    """
    if auth_key != auth:
        raise ValueError('Incorrect/Missing authentication key')
    if isinstance(server_url, type(None)):
        server_url = server
    elif server_url not in valid_servers:
        raise NameError('Incorrect/Missing server name')
    auth_key = {'Authorization': str(auth_key)}
    # initial request // used to collect data during recursion or as output of single API call
    in_req = requests.get(f'https://{server_url}/{endpoint}?{argstring}', headers=auth_key)
    if in_req.headers.get('content-type') != 'application/json; charset=UTF-8':
        raise ValueError('Warning!: Potentially missing endpoint. Data not being returned by server.')
    if 400 <= in_req.status_code <= 499:
        raise NameError(f'Request error (client-side/Error might be endpoint): {in_req.status_code}')
    elif 500 <= in_req.status_code <= 599:
        raise NameError(f'Request error (server-side): {in_req.status_code}')
    in_json = in_req.json()
    # checking that the request contains data
    hits = 'hits' in in_json.keys()
    results = 'results' in in_json.keys()
    contains_data = hits | results
    if collect_all is False:
        if hits and (len(in_json['hits']) == 0):
            print('Warning!: Data has "hits" but length of data is 0')
        elif results and (len(in_json['results']) == 0):
            print('Warning!: Data has "results" but length of data is 0')
        return in_json
    elif collect_all and not contains_data:
        return
    elif collect_all and contains_data:
        # initial dict for collecting new json data
        data_json = {k: v if isinstance(v, list) else [v] for k, v in in_json.items()}
        del data_json['_scroll_id']
        # recursion during collection
        scroll_id = in_json['_scroll_id']
        fetching_page = '&fetch_all=True&page='
        page = fetching_page + str(curr_page)
        to_scroll = 'scroll_id=' + scroll_id + page
        in_req = get_outbreak_data(endpoint, to_scroll, server_url=server_url, collect_all=True, curr_page=curr_page+1)
        if not isinstance(in_req, type(None)):
            if hits and len(in_req['hits']) == 0:
                print('Warning!: Recursion step has "hits" key but empty data value')
            elif results and len(in_req['results']) == 0:
                print('Warning!: Recursion step has "results" key but empty data value')
            in_req = {k: v if isinstance(v, list) else [v] for k, v in in_req.items()}
        for k in data_json.keys():
            try:
                data_json[k].extend(in_req[k])
            except TypeError:
                continue
        return data_json
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
# def cases_by_location(location, server=server, auth=auth, pull_smoothed=0):
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
    :param location: A string or list of strings, separate multiple locations by ","
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
        raw_data = get_outbreak_data(covid19_endpoint, args, collect_all=True)
        df = pd.DataFrame(raw_data['hits'])
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


def prevalence_by_location(location, startswith=None, server=server, auth=auth):
    lins = get_outbreak_data('genomics/prevalence-by-location-all-lineages',
                             f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0')
    df = pd.DataFrame(lins['results'])

    """Loads prevalence data from a location
            Arguments:
                :param location: A string
                :param num_pages: For every value >= 0, returns 1000 obs. (paging)
                :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
            Returns:
                A pandas dataframe"""

    if startswith is not None:
        return df.loc[df['lineage'].str.startswith(startswith)]
    return df


def lineage_mutations(pango_lin, mutation=None, freq=0.8, server=server, auth=auth):
    """Retrieves data from all mutations in a specified lineage above a frequency threshold.
       Mutiple queries for lineages and mutations can be separated by ','
    
          Arguments:
             :param pango_lin: A string or list; loads data for all mutations in a specified PANGO lineage 
             :param mutation: A string or list; loads data for lineages containing a specified mutation
             :param freq: a number between 0 and 1 specifying the frequency threshold above which to return mutations (default = 0.8)
          Returns:
              A pandas dataframe"""

    # Turns any string input into list format: most universal

    if isinstance(pango_lin, str):
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
    raw_data = get_outbreak_data('genomics/lineage-mutations', f'pangolin_lineage={lineages}', collect_all=False)
    df = pd.DataFrame(raw_data['results'][lineages])
    if freq != 0.8:
        if isinstance(freq, float) and freq > 0 and freq < 1:
            return df.loc[df['prevalence'] >= freq]
    else:
        return df
