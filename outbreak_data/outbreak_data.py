import pandas as pd
import requests
import warnings

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = ***REMOVED***  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'
test_server = 'test.outbreak.info'


def get_outbreak_data(endpoint, argstring, server=server, auth=auth, collect_all=False, curr_page=0):
    """
    Receives raw data using outbreak API.
    :param endpoint: directory in server the data is stored
    :param argstring: feature arguments to provide to API call
    :param server: Server to request from
    :param auth: Auth key (defaults to acceptable state)
    :param collect_all: if True, returns all data.
    :param curr_page: iterator state for paging
    :return: A request object containing the raw data
    """
    # To secure against None type
    if isinstance(server, type(None)):
        server = server
    auth = {'Authorization': str(auth)}
    # initial request // used to collect data during recursion or as output of single API call
    in_req = requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth)
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
            warnings.warn('Warning!: Data has "hits" but length of data is 0')
        elif results and (len(in_json['results']) == 0):
            warnings.warn('Warning!: Data has "results" but length of data is 0')
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
        in_req = get_outbreak_data(endpoint, to_scroll, server=server, collect_all=True, curr_page=curr_page+1)
        if not isinstance(in_req, type(None)):
            if hits and len(in_req['hits']) == 0:
                warnings.warn('Warning!: Recursion step has "hits" key but empty data value')
            elif results and len(in_req['results']) == 0:
                warnings.warn('Warning!: Recursion step has "results" key but empty data value')
            in_req = {k: v if isinstance(v, list) else [v] for k, v in in_req.items()}
        for k in data_json.keys():
            try:
                data_json[k].extend(in_req[k])
            except TypeError:
                continue
        return data_json


def cases_by_location(location, server=server, auth=auth, pull_smoothed=0):
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
    if pull_smoothed == 0:
        confirmed='confirmed_numIncrease'
    elif pull_smoothed == 1:
        confirmed='confirmed_rolling'
    elif pull_smoothed == 2:
        confirmed='confirmed_rolling, confirmed_numIncrease'
    else:
        raise Exception("invalid parameter value for pull_smoothed!")
    try:
        locations = '(' + ' OR '.join(location) + ')'
        args = f'q=location_id:{locations}&sort=date&fields=date,{confirmed},admin1&{nopage}'
        raw_data = get_outbreak_data(covid19_endpoint, args, collect_all=True)
        df = pd.DataFrame(raw_data['hits'])
        refined_table=df.drop(columns=['_score', 'admin1'], axis=1)
        for i in location:  # checks each entry in location for invalid location ids after request
                check = i[0:2] #checks for first 3 letters from string input in df; if they're there, the df passed
                valid_loc = df.loc[df['_id'].str.startswith(check)]
                if valid_loc.empty:
                    raise Exception('{} is not a valid location ID'.format(i))
        if not df.empty:
            return df
            return refined_table
    except:
        for i in location:
            raise Exception('{} is not a valid location ID'.format(i))


def prevalence_by_location(location, startswith=None, server=server, auth=auth):

    """Loads prevalence data from a location
            Arguments:
                :param location: A string
                :param num_pages: For every value >= 0, returns 1000 obs. (paging)
                :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
            Returns:
                A pandas dataframe"""
                
    lins = get_outbreak_data('genomics/prevalence-by-location-all-lineages',
                             f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0')
    df = pd.DataFrame(lins['results'])
    if startswith is not None:
        return df.loc[df['lineage'].str.startswith(startswith)]
    return df


def lineage_mutations(pango_lin, mutation=None, freq=0.8, server=server, auth=auth):
    """Retrieves data from all mutations in a specified lineage above a frequency threshold.
       - Mutiple queries for lineages and mutations can be separated by ","
       - Use 'OR' in a string to return overlapping mutations in multiple lineages: 'BA.2 OR BA.1'
       - param mutation is only useful for one lineage + mutation1 + mutation2 .... combinations

          Arguments:
             :param pango_lin: A string or list; loads data for all mutations in a specified PANGO lineage 
             :param mutation: A string or list; loads data of mutations for sequences classified as a specified PANGO lineage with mutation
             :param freq: a number between 0 and 1 specifying the frequency threshold above which to return mutations (default = 0.8)
          Returns:
              A pandas dataframe"""
    # Turns any string input into list format: most universal
    OR_stat = False
    if isinstance(pango_lin, list) and isinstance(mutation, type(list)) or isinstance(mutation,type(None)):
        pass
    if isinstance(pango_lin, str):
        if ' OR ' in pango_lin: #lineages with OR logic
            OR_stat = True
            pango_lin = pango_lin.replace(" OR ", ",")
            pango_lin = list(pango_lin.split(","))  # deals with string format for pango_lin
        else:
            pango_lin = pango_lin.replace(" ", "")  # for just returning lineages 
            pango_lin = list(pango_lin.split(",")) 
            
    if isinstance(mutation, str):
            mutation = mutation.replace(" ", "")
            mutation = list(mutation.split(","))   # deals with string format for mutations
   
    if OR_stat and isinstance(mutation, type(None)):
        lineages = '' + ' OR '.join(pango_lin)
    elif mutation is None:
        lineages = '' + ','.join(pango_lin)
    else:
        lineages = '' + pango_lin[0] + ' AND ' + ' AND '.join(mutation) + ''   # ability to handle more complex queries coming in later function
  
    raw_data = get_outbreak_data('genomics/lineage-mutations', f'pangolin_lineage={lineages}', collect_all=False)
    
    if OR_stat == False and mutation is None: # no OR logic. just lineages
        for i in pango_lin: # Returns multiple lineages using ","
            if i == pango_lin[0]:
                df = pd.DataFrame(raw_data['results'][i])
            else:
                newdf = pd.DataFrame(raw_data['results'][i]) # append each dfs
                df = pd.concat([df, newdf], sort=False)  
    else:
         df = pd.DataFrame(raw_data['results'][lineages]) 
    if freq != 0.8:
        if isinstance(freq, float) and freq > 0 and freq < 1:
            return df.loc[df['prevalence'] >= freq]
    else:
        return df
    
def global_prevalence(pango_lin, mutations=None, cumulative=None, server=test_server):
   
    # Takes multiple mutations but only one pango_lin
    
    if isinstance(mutations, type(list)) or isinstance(mutations,type(None)):
        pass
    elif isinstance(mutations, str):
         mutations = mutations.replace(" ", "")
         mutations = list(mutations.split(","))   # deals with string format for mutations
    if mutations != None and cumulative == True:
        mutations = '' + ','.join(mutations)
        query = '' + pango_lin + '&' + f'mutations={mutations}' + '&' + 'cumulative=true'
    elif mutations != None:
        mutations = '' + ','.join(mutations)
        query =  '' + pango_lin + '&' + f'mutations={mutations}'
    elif cumulative == True:
        query = '' + pango_lin + '&' + 'cumulative=true'
    else:
        query = '' + pango_lin
      
    raw_data = get_outbreak_data('genomics/global-prevalence', f'pangolin_lineage={query}')
   
    if cumulative:
        data = {'Values' : raw_data['results']}
        df = pd.DataFrame(data) 
    else:
        df = pd.DataFrame(raw_data['results'])
    return df


def sequence_counts(location=None, cumulative=None, sub_admin=None, server=test_server):
    
    if location and cumulative and sub_admin:
        query = '' + f'location_id={location}&cumulative=true&subadmin=true'
    elif location and cumulative:
        query = '' + f'location_id={location}&cumulative=true'
    elif cumulative:
        query = '' + 'cumulative=true'
    elif location:
        query = '' + f'location_id={location}'
    else:
        query = ''
            
    raw_data = get_outbreak_data('genomics/sequence-count', f'{query}')
    
    if cumulative and sub_admin is None:
        data = {'Values' : raw_data['results']}
        df = pd.DataFrame(data) 
    else:
        df = pd.DataFrame(raw_data['results'])
    return df

def mutation_across_lineage(mutation, location=None, pango_lin=None, freq=None, server=test_server):  #Under what conditions would it be usefule to have mutations=None?
    
    if isinstance(mutation, type(list)):
        pass
    elif isinstance(mutation, str):
         mutation = mutation.replace(" ", "")
         mutation = list(mutation.split(","))
    
    mutations = '' + ' AND '.join(mutation) + ''   
         
    if location and pango_lin:
        query = '' + f'mutations={mutations}&location_id={location}&pangolin_lineage={pango_lin}'
    elif location:
        query = '' + f'mutations={mutations}&location_id={location}'
    else:
        query = '' + f'mutations={mutations}'
        
    raw_data = get_outbreak_data('genomics/mutations-by-lineage', f'{query}')
    
    for i in mutation: # Returns multiple lineages using ","
        if i == mutation[0]:
            df = pd.DataFrame(raw_data['results'][i])
        else:
            newdf = pd.DataFrame(raw_data['results'][i]) # append each df
            df = pd.concat([df, newdf], sort=False)  
    
    if isinstance(freq, float) and freq > 0 and freq < 1:
        return df.loc[df['prevalence'] >= freq]
    return df
