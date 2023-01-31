import sys
import requests
import warnings
import pandas as pd

import authenticate_user

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'
test_server = 'test.outbreak.info'
def check_user_authentication():
    """
    Get the authorization token.
    :return token: the users authorization token
    """
    try:
        token = authenticate_user.get_authentication()
    except:
        print("Issue retrieving token, please reauthenticate.")
        sys.exit(1)
    if token == "":
        print("Issue retrieving token, please reauthenticate.")
        sys.exit(1)
    return(token)

def get_outbreak_data(endpoint, argstring, server=server, auth=None, collect_all=False, curr_page=0):
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
    
    if auth is None:
        #check the authentication
        token = check_user_authentication()
    else:
        token = auth
    token = 'Bearer ' + token
    auth = {'Authorization': str(token)}
    # initial request // used to collect data during recursion or as output of single API call
    url = f'https://{server}/{endpoint}?{argstring}'
    in_req = requests.get(url, headers=auth)
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


def cases_by_location(location, server=server, auth=None, pull_smoothed=0):
    """
    Loads data from a location if input is a string, or from multiple locations
    if location is a list of string locations.
    Since this API endpoint supports paging, collect_all is used to return all data.
    :param location: A string or list of strings, separate multiple locations by ","
    :param pull_smoothed: For every value >= 0, returns 1000 obs. (paging)
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


def prevalence_by_location(location, startswith=None, ndays=2048, nday_threshold=0, other_threshold=0, other_exclude=None, cumulative=None, server=server, auth=None):

    """Loads prevalence data from a location
            Arguments:
                :param location: A string
                :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
                :param other_threshold (Default: 0) Minimum prevalence threshold below which lineages must be accumulated under "Other".
                :param nday_threshold (Default: 0) Minimum number of days in which the prevalence of a lineage must be below other_threshold to be accumulated under "Other".
                :param ndays (Default: 2048) The number of days before the current date to be used as a window to accumulate linegaes under "Other".
                :param other_exclude: Comma separated lineages that are NOT to be included under "Other" even if the conditions specified by the three thresholds above are met.
                :param cumulative: (Default: false) If true return the cumulative prevalence.
                :return: A pandas dataframe"""
                
    query =  f'location_id={location}&sort=date&ndays={ndays}&nday_threshold={nday_threshold}&other_threshold={other_threshold}'
   
    if cumulative:
        query = query + '&' + 'cumulative=true'
    if other_exclude:
        other_exclude = other_exclude.replace(" ", "")
        query = query + '&' + f'other_exclude={other_exclude}'
        
    lins = get_outbreak_data('genomics/prevalence-by-location-all-lineages', query)
    df = pd.DataFrame(lins['results'])
    if startswith is not None:
        return df.loc[df['lineage'].str.startswith(startswith)]
    return df


def lineage_mutations(pango_lin, mutations=None, freq=0.8, server=server, auth=None):

    """Retrieves data from all mutations in a specified lineage above a frequency threshold.
       - Mutiple queries for lineages and mutations can be separated by ","
       - Use 'OR' in a string to return overlapping mutations in multiple lineages: 'BA.2 OR BA.1'
       - param mutation is only useful for one lineage + mutation1 + mutation2 .... combinations

          Arguments:
             :param pango_lin: A string or list; loads data for all mutations in a specified PANGO lineage 
             :param mutation: A string or list; loads data of mutations for sequences classified as a specified PANGO lineage with mutation
             :param freq: A number between 0 and 1 specifying the frequency threshold above which to return mutations (default = 0.8)
             :return: A pandas dataframe"""

    # Turns any string input into list format: most universal
    if isinstance(pango_lin, str) is True:
      if 'OR' in pango_lin:
          lineages = pango_lin.split('OR')
          lineages = "OR".join(lineages)
      else:
          lineages = pango_lin.replace(" ", "")
          lineages = lineages.split(',')
          lineages = ",".join(lineages)
    elif isinstance(pango_lin, list):
         lineages = ",".join(pango_lin)
                  
    if mutations:
        if isinstance(mutations, str) is True:
            mutations = mutations.replace(" ", "")
            mutations = list(mutations.split(","))   # deals with string format for mutations

        if isinstance(mutations, list) is True:
            mutations = " AND ".join(mutations)
        mutations = " AND " + mutations
        lineages = '' + lineages + '' + mutations # fixed function
    raw_data = get_outbreak_data('genomics/lineage-mutations', f'pangolin_lineage={lineages}', collect_all=False)
    key_list = raw_data['results']
    key_list = list(key_list)

    for i in key_list: # Returns multiple lineages using ","
        if i == key_list[0]:
            df = pd.DataFrame(raw_data['results'][i])
        else:
            newdf = pd.DataFrame(raw_data['results'][i]) # append each dfs
            df = pd.concat([df, newdf], sort=False)  

    if freq != 0.8:
        if isinstance(freq, float) and freq > 0 and freq < 1:
            return df.loc[df['prevalence'] >= freq]
    else:
        return df
    

def global_prevalence(pango_lin, mutations=None, cumulative=None, server=test_server):
   
    """Returns the global daily prevalence of a PANGO lineage
       
       Arguments:
        :param pangolin_lineage: (Required).
        :param mutations: (Optional). Comma separated list of mutations.
        :param cumulative: (Optional). If true returns the cumulative global prevalence since the first day of detection.
        :return: A pandas dataframe."""
    if mutations:
        if isinstance(mutations, list):
            mutations = ','.join(mutations)
        elif isinstance(mutations, str):
             mutations = mutations.replace(" ", "")
       
    query = '' + pango_lin
      
    if mutations:
        query =  query + '&' + f'mutations={mutations}' 
    if cumulative:
        query = query + '&' + 'cumulative=true'
      
    raw_data = get_outbreak_data('genomics/global-prevalence', f'pangolin_lineage={query}')
   
    if cumulative:
        data = {'Values' : raw_data['results']}
        df = pd.DataFrame(data) 
    else:
        df = pd.DataFrame(raw_data['results'])
    return df


def sequence_counts(location=None, cumulative=None, sub_admin=None, server=test_server):
    """Returns number of sequences per day by location

        Arguments:
        :param location_id: (Optional). If not specified, the global total counts are returned.
        :param cumulative: (Optional). If true returns the cumulative number of sequences till date.
        :param subadmin: (Optional). If true and cumulative=true, returns the cumulative number of sequences for the immedaite lower admin level.
        :return: A pandas dataframe."""
        
    query = ''    
    if location:
        query = query + f'location_id={location}'
    if cumulative:
        query = query +  '&' + 'cumulative=true'
    if sub_admin:
        query = query + '&' + 'subadmin=true'
            
    raw_data = get_outbreak_data('genomics/sequence-count', f'{query}')
     
    if cumulative or sub_admin:
        data = {'Values' : raw_data['results']}
        df = pd.DataFrame(data) 
    else:
        df = pd.DataFrame(raw_data['results'])
    return df


def mutations_by_lineage(mutation, location=None, pango_lin=None, freq=None, server=test_server):
    """Returns the prevalence of a mutation or series of mutations across specified lineages by location

        Arguments:
        :param mutations: (Optional). List of mutations. 
        :param location_id: (Optional). If not specified, return most recent date globally.
        :param pangolin_lineage: (Optional). If not specfied, returns all Pango lineages containing that mutation.
        :param frequency: (Optional) Minimimum frequency threshold for the prevalence of a mutation in a lineage.
        :return: A pandas dataframe."""
    
    if isinstance(mutation, list):
        pass
    elif isinstance(mutation, str):
         mutation = mutation.replace(" ", "")
         mutation = list(mutation.split(","))
    
    mutations = '' + ','.join(mutation) + ''   
    if location is not None and pango_lin is not None:
        query = '' + f'mutations={mutations}&location_id={location}&pangolin_lineage={pango_lin}'
    elif location is not None:
        query = '' + f'mutations={mutations}&location_id={location}'
    elif pango_lin is not None:
        query = '' + f'mutations={mutations}&pangolin_lineage={pango_lin}'
    else:
        query = '' + f'mutations={mutations}'

    raw_data = get_outbreak_data('genomics/mutations-by-lineage', f'{query}')
    df = pd.DataFrame(raw_data['results'][mutations])

    if isinstance(freq, float) and freq > 0 and freq < 1:
        return df.loc[df['prevalence'] >= freq]
    return df
    
def daily_prev_by_location(pango_lin, location='USA', mutations=None, cumulative=None):
    """Returns the daily prevalence of a PANGO lineage by location.
   
       Arguments:
        :param: pango_lin (Required). List of lineages separated by ,
        :param: location_id (Optional). Default location: USA
        :param: mutations (Optional). List of mutations separated by AND
        :param: cumulative (Optional). If true returns the cumulative global prevalence since the first day of detection.
        :return: A pandas dataframe."""
    
    if isinstance(pango_lin, str):
       pango_lin = pango_lin.replace(" ", "")
     
    elif isinstance(pango_lin, list):
        pango_lin = ','.join(pango_lin)

    if mutations:
        if isinstance(mutations, list):
            pass
        elif isinstance(mutations, str):
             mutations = mutations.replace(" ", "")
             mutations = list(mutations.split(","))
        mutations = '' + ' AND '.join(mutations) + ''   
      
    query = pango_lin + '&' + f'location_id={location}'
    
    if mutations:
        query = query + '&' + f'mutations={mutations}'
    if cumulative:
        query = query + '&' + 'cumulative=true'
         
    raw_data = get_outbreak_data('genomics/prevalence-by-location', f'pangolin_lineage={query}', collect_all=False)
    key_list = raw_data['results']
    key_list = list(key_list)
    
    if cumulative:
        for i in key_list:
            if i == key_list[0]:
                 data = {'Values' : raw_data['results'][i]}
                 df = pd.DataFrame(data) 
            else:
                newdf = {'Values' : raw_data['results'][i]}
                df = pd.concat([data, newdf], sort=False)  
    else:
        for i in key_list:
            if i == key_list[0]:
                df = pd.DataFrame(raw_data['results'][i])
            else:
                newdf = pd.DataFrame(raw_data['results'][i]) # append each df
                df = pd.concat([df, newdf], sort=False)  
    return df
 


def lineage_by_sub_admin(pango_lin, mutations=None, location=None, ndays=None, detected=None):
    """Cumulative prevalence of a PANGO lineage by the immediate admin level of a location

        Arguments:
        :param pangolin_lineage: (Required). A list or string. List of lineages separated by ,
        :param mutations: (Optional). A string or list of strings. Uses AND logic.
        :param location_id: (Optional). A string. If not specified, returns cumulative prevalence at the country level globally.
        :param ndays: (Optional). An integer. Specify number of days from current date to calculative cumuative counts. If not specified, there is no limit on the window.
        :param detected: (Optional). If true returns only if at least found in location
        :return: A pandas dataframe."""
        
    if isinstance(pango_lin, str):
        pango_lin = pango_lin.replace(" ", "")
    elif isinstance(pango_lin, list):
         pango_lin = ','.join(pango_lin)
         
    if mutations:
        if isinstance(mutations, list):
            pass
        elif isinstance(mutations, str):
             mutations = mutations.replace(" ", "")
             mutations = list(mutations.split(","))
        mutations = '' + ' AND '.join(mutations) + ''   
    
    if mutations:
        query = '' + pango_lin + '&' + f'mutations={mutations}'
    if location:
        query = query + '&' + f'location_id={location}'
    if ndays > 0:
        query = query + '&' + f'ndays={ndays}'
        
    raw_data = get_outbreak_data('genomics/lineage-by-sub-admin-most-recent', f'pangolin_lineage={query}', collect_all=False)
    key_list = raw_data['results']
    key_list = list(key_list)
    
    for i in key_list:
        if i == key_list[0]:
            df = pd.DataFrame(raw_data['results'][i])
        else:
            newdf = pd.DataFrame(raw_data['results'][i]) # append each df
            df = pd.concat([df, newdf], sort=False)
    return df
    

def collection_date(pango_lin, mutations=None, location=None):
    """Most recent collection date by location

    Arguments:
    :param pango_lin: A string. (Required).
    :param mutations: (Optional). A string or list of strings. Comma separated list of mutations.
    :param location: (Optional). If not specified, return most recent date globally.
    :return: A pandas dataframe."""
    if mutations:
        if isinstance(mutations, list):
            mutations = ','.join(mutations)
        elif isinstance(mutations, str):
             mutations = mutations.replace(" ", "")
    
    query = pango_lin
    if mutations:
        query = query + '&' + f'mutations={mutations}'
    if location:
        query = query + '&' + f'location_id={location}'
        
    raw_data = get_outbreak_data('genomics/most-recent-collection-date-by-location', f'pangolin_lineage={query}', collect_all=False)
   
    data = {'Values' : raw_data['results']}
    df = pd.DataFrame(data) 
    return df


def submission_date(pango_lin, mutations=None, location=None):
    """Returns the most recent submission date by location

     Arguments:
     :param pango_lin: A string. (Required).
     :param mutations: (Optional). A string or list of strings. Comma separated list of mutations.
     :param location: (Optional). If not specified, return most recent date globally.
     :return: A pandas dataframe."""
    if mutations:
         if isinstance(mutations, list):
             mutations = ','.join(mutations)
         elif isinstance(mutations, str):
              mutations = mutations.replace(" ", "")
     
    query = pango_lin
    if mutations:
         query = query + '&' + f'mutations={mutations}'
    if location:
         query = query + '&' + f'location_id={location}'
         
    raw_data = get_outbreak_data('genomics/most-recent-submission-date-by-location', f'pangolin_lineage={query}', collect_all=False)
    
    data = {'Values' : raw_data['results']}
    df = pd.DataFrame(data) 
    return df
 
    
def mutation_details(mutations):
    """ Returns details of a mutation.
    
    Arguments:
    :param mutations: (Required). Comma separated list of mutations.
    :return: A pandas dataframe."""
    
    if isinstance(mutations, str):
         mutations = mutations.replace(" ", "")
    elif isinstance(mutations, list):
         mutations = ','.join(mutations)
   
    raw_data = get_outbreak_data('genomics/mutation-details', f'mutations={mutations}', collect_all=False)
    
    r = raw_data['results']
    keys = list(r[0])
   
    for i in r: # for each seperate result
        values = list(i.values())
        if i == r[0]:
            df=pd.DataFrame({"Key": keys,
                 "Values":values})
        else:
                newdf = pd.DataFrame({"Key": keys,
                     "Values":values}) # append each df
                df = pd.concat([df, newdf], axis=1, sort=False)
    return df


def daily_lag(location=None):
    """Return the daily lag between collection and submission dates by location

    Arguments:
    :param location_id: (Optional). If not specified, return lag globally.
    :return: A pandas dataframe.
    """
    query = ''
    if location:
        query =  '&' + f'location_id={location}'
        
    raw_data = get_outbreak_data('genomics/collection-submission', query, collect_all=False)
    
    r = raw_data['results']
    keys = tuple(r[0])
    
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"Key": keys,
                 "Values":values})
        else:
                newdf = pd.DataFrame({"Key": keys,
                     "Values":values}) # append each df
                df = pd.concat([df, newdf], axis=1, sort=False)
    return df
     

def wildcard_lineage(name):
    """Match lineage name using wildcards. 

    Arguments:
    :param name: (Required). A string. Must use * at end of string. Supports wildcards. (Example: b.1*, ba.2*)
    :return: A pandas dataframe."""
    
    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/lineage', query, collect_all=False)
    r = raw_data['results']
    keys = tuple(r[0])
    
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"Key": keys,
                 "Values":values})
        else:
                newdf = pd.DataFrame({"Key": keys,
                     "Values":values}) # append each df
                df = pd.concat([df, newdf], axis=1, sort=False)
    return df
     

def wildcard_location(name):
    """Match location name using wildcards. 

    Arguments:
    :param name: (Required). A string. Must use * at end of string. Supports wildcards. (Example: united*)
    :return: A pandas dataframe."""
    
    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/location', query, collect_all=False)
    r = raw_data['results']
    keys = tuple(r[0])
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"Key": keys,
                 "Values":values})
        else:
                newdf = pd.DataFrame({"Key": keys,
                     "Values":values}) # append each df
                df = pd.concat([df, newdf], axis=1, sort=False)
    return df
     

def location_details(location):
    """Get location details using location ID.
     
    Arguments:
    :param location: A string. (Required).
    :return: A pandas dataframe."""
   
    query = '' + '&' + f'id={location}'
    raw_data = get_outbreak_data('genomics/location-lookup', query, collect_all=False)
    data = {'Values' : raw_data['results']}
    df = pd.DataFrame(data) 
    return df

    
def wildcard_mutations(name):
    """Match mutations using wildcards.
    
     Arguments:
     :param name: (Required)  A string. Must use * at end of string. Supports wildcards. (Example: s:e484*)
     :return: A pandas dataframe."""

    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/mutations', query, collect_all=False)
    r = raw_data['results']
    keys = tuple(r[0])
    
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"Key": keys,
                 "Values":values})
        else:
                newdf = pd.DataFrame({"Key": keys,
                     "Values":values}) # append each df
                df = pd.concat([df, newdf], axis=1, sort=False)
    return df
