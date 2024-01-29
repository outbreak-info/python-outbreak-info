import sys
import requests
import warnings
import pandas as pd

from outbreak_data import authenticate_user

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

    Arguments: 
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
    print(url)

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
    if location is a list of string locations. Since this API endpoint supports paging, collect_all is used to return all data.

    Arguments:
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
        return refined_table
    
    except:
        for i in location:
            raise Exception('{} is not a valid location ID'.format(i))


def all_lineage_prevalences(location, ndays=180, nday_threshold=10, other_threshold=0.05, other_exclude=None, cumulative=None, server=server, auth=None, startswith=None):
    """
    Loads prevalence data from a location

    Arguments:
     :param location: A string
     :param other_threshold (Default: 0) Minimum prevalence threshold below which lineages must be accumulated under "Other".
     :param nday_threshold (Default: 0) Minimum number of days in which the prevalence of a lineage must be below other_threshold to be accumulated under "Other".
     :param ndays (Default: 180) The number of days before the current date to be used as a window to accumulate lineages under "Other".
     :param other_exclude: Comma separated lineages that are NOT to be included under "Other" even if the conditions specified by the three thresholds above are met.
     :param cumulative: (Default: false) If true return the cumulative prevalence.:param startswith: A string; loads data for all lineages beginning with first letter(s) of name
     :return: A pandas dataframe
    """
                
    query =  f'location_id={location}&ndays={ndays}&nday_threshold={nday_threshold}&other_threshold={other_threshold}'
   
    if cumulative:
        query = query + '&' + 'cumulative=true'
    if other_exclude:
        other_exclude = other_exclude.replace(" ", "")
        query = query + '&' + f'other_exclude={other_exclude}'
        
    lins = get_outbreak_data('genomics/prevalence-by-location-all-lineages', query)
    df = pd.DataFrame(lins['results'])
    if startswith:
        return df.loc[df['lineage'].str.startswith(startswith)]
    return df


### Helper function for dealing with all 'q' queries
def pangolin_crumbs(pango_lin, mutations=None,lin_prefix=True):
    if lin_prefix:
        query = 'lineages=None&'
    else:
        query = ''
    if mutations:
        query = query + f'mutations={mutations}&'
    query = query + f'q=pangolin_lineage_crumbs:*;{pango_lin};*'
    return query


def lineage_mutations(pango_lin=None, lineage_crumbs=False, mutations=None, freq=0.8, server=server, auth=None):  ###
    """Retrieves data from all mutations in a specified lineage above a frequency threshold.
       - Use 'OR' in a string to return overlapping mutations in multiple lineages: 'BA.2 OR BA.1'

          Arguments:
             :param pango_lin: A string; loads data for all mutations in a specified PANGO lineage
             :param lineage_crumbs: If true returns data for descendant lineages of pango_lin. Include the wildcard '*' in string to return info on all related lineages.
             :param mutations: A string; loads mutation data for the specified sequence under the specified PANGO lineage 
             :param freq: A number between 0 and 1 specifying the frequency threshold above which to return mutations (default = 0.8)
             :return: A pandas dataframe"""

    # Use strings, no reason to use list format anymore
    
    if lineage_crumbs:
        query = pangolin_crumbs(pango_lin)
                
    else:
        query = f'lineages={pango_lin}'
        if 'OR' in pango_lin:
          lineages = pango_lin.split('OR')
          query = "OR".join(lineages)
        if mutations:
            query = '&' + f'mutations={mutations}' + query 
        
    if freq!=0.8:
        query = query + f'&frequency={freq}'
    raw_data = get_outbreak_data('genomics/lineage-mutations', f'{query}', collect_all=False)
    key_list = raw_data['results']
    if len(key_list) == 0:
        raise TypeError('No matches for query found')
    
    key_list = raw_data['results']
    key_list = list(key_list)
    df = pd.DataFrame(raw_data['results'][key_list[0]])
       
    return df
    

def global_prevalence(pango_lin, mutations=None, cumulative=None, lineage_crumbs=False, server=server):
   
    """Returns the global daily prevalence of a PANGO lineage
       
       Arguments:
        :param pangolin_lineage: (Required).
        :param mutations: (Somewhat optional). Comma separated list of mutations.
        :param cumulative: (Somewhat optional). If true returns the cumulative global prevalence since the first day of detection.
        :return: A pandas dataframe."""

    if lineage_crumbs:
        query = pangolin_crumbs(pango_lin)   
    else:
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
    if lineage_crumbs:
        # using a modified formulation to access the crumbs 
        raw_data = get_outbreak_data('genomics/prevalence-by-location', query, collect_all=False)
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
    else:
        raw_data = get_outbreak_data('genomics/global-prevalence', f'pangolin_lineage={query}')
        if cumulative:
            data = {'Values' : raw_data['results']}
            df = pd.DataFrame(data) 
        else:
            df = pd.DataFrame(raw_data['results'])
    return df

def sequence_counts(location=None, cumulative=None, sub_admin=None, server=server):
    """Returns number of sequences per day by location

    Arguments:
     :param location: (Somewhat optional). If not specified, the global total counts are returned.
     :param cumulative: (Somewhat optional). If true returns the cumulative number of sequences till date.
     :param subadmin: (Somewhat optional). If true and cumulative=true, returns the cumulative number of sequences for the immedaite lower admin level.
     :return: A pandas dataframe.
    """
        
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

def mutations_by_lineage(mutation=None, location=None, pango_lin=None, lineage_crumbs=False, datemin=None,  datemax=None, freq=None, server=server):
    """Returns the prevalence of a mutation or series of mutations across specified lineages by location

    Arguments:
     :param mutations: (Optional). List or string of mutations separated by ",". 
     :param location_id: (Optional). A string; If not specified, return most recent date globally.
     :param pangolin_lineage: (Optional). If not specfied, returns all Pango lineages containing that mutation.
     :param frequency: (Optional) Minimimum frequency threshold for the prevalence of a mutation in a lineage.
     :param datemin: (Optional). A string representing the first cutoff date for returned date. Must be in YYYY-MM-DD format and be before 'datemax'
     :param datemax: (Optional). A string representing the second cutoff date. Must be in YYY-MM-DD format and be after 'datemin'
     :return: A pandas dataframe.
    """
    
    if mutation: 
        if isinstance(mutation, str):
             mutation = mutation.replace(" ", "")
             mutation = list(mutation.split(","))
        mutation = '' + ' AND '.join(mutation) + ''   
        query = f'mutations={mutation}'
            
    if pango_lin and lineage_crumbs:
        query = pangolin_crumbs(pango_lin)

    if location:
        query = query + f'&location_id={location}'
    if datemin and datemax:
        query = query + f'&datemin={datemin}&datemax={datemax}'

    raw_data = get_outbreak_data('genomics/mutations-by-lineage', f'{query}')
    
    key_list = raw_data['results']
    key_list = list(key_list)
    df = pd.DataFrame(raw_data['results'][key_list[0]])
       
    if isinstance(freq, float) and freq > 0 and freq < 1:
        return df.loc[df['prevalence'] >= freq]
    return df


def prevalence_by_location(pango_lin, location, mutations=None,  datemin=None, lineage_crumbs=False, 
                           datemax=None, cumulative=None, server=server):
    """Returns the daily prevalence of a PANGO lineage by location.
   
       Arguments:
        :param pango_lin: (Required). List of lineages separated by ,
        :param location_id: (Somewhat optional). Default location: USA
        :param mutations: (Somewhat optional). List of mutations separated by AND
        :param cumulative: (Somewhat optional). If true returns the cumulative global prevalence since the first day of detection.
        :param datemin: (Optional). A string representing the first cutoff date for returned date. Must be in YYYY-MM-DD format and be before 'datemax'
        :param datemax: (Optional). A string representing the second cutoff date. Must be in YYY-MM-DD format and be after 'datemin'
        :return: A pandas dataframe."""
    if lineage_crumbs:
        query = pangolin_crumbs(pango_lin)  
        query = query + '&' + f'location_id={location}' 
    else:
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
    if datemin and datemax:
        query = query + f'&datemin={datemin}&datemax={datemax}'
   
    if lineage_crumbs:
        raw_data = get_outbreak_data('genomics/prevalence-by-location', query, collect_all=False)
    else:
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


def lineage_by_sub_admin(pango_lin, mutations=None, location=None, ndays=0, detected=None, server=server):
    """Cumulative prevalence of a PANGO lineage by the immediate admin level of a location

        Arguments:
        :param pangolin_lineage: (Required). A list or string. List of lineages separated by ,
        :param mutations: (Somewhat optional). A string or list of strings. Uses AND logic.
        :param location_id: (Somewhat optional). A string. If not specified, returns cumulative prevalence at the country level globally.
        :param ndays: (Somewhat optional). An integer. Specify number of days from current date to calculative cumuative counts. If not specified, there is no limit on the window.
        :param detected: (Somewhat optional). If true returns only if at least found in location
        :return: A pandas dataframe."""
        
    if isinstance(pango_lin, str):
        pango_lin = pango_lin.replace(" ", "")
    elif isinstance(pango_lin, list):
         pango_lin = ','.join(pango_lin)
    query = pango_lin
         
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
    

def collection_date(pango_lin, mutations=None, location=None, server=server):
    """Most recent collection date by location

    Arguments:
     :param pango_lin: A string. (Required).
     :param mutations: (Somewhat optional). A string or list of strings. Comma separated list of mutations.
     :param location: (Somewhat optional). If not specified, return most recent date globally.
     :return: A pandas dataframe.
    """
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


def submission_date(pango_lin, mutations=None, location=None, server=server):
    """Returns the most recent submission date by location

     Arguments:
     :param pango_lin: A string. (Required).
     :param mutations: (Somewhat optional). A string or list of strings. Comma separated list of mutations.
     :param location: (Somewhat optional). If not specified, return most recent date globally.
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
 
   
def mutation_details(mutations, server=server):
    """ Returns details of a mutation.
    
    Arguments:
     :param mutations: (Required). Comma separated list of mutations.
     :return: A pandas dataframe.
    """
    
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


def daily_lag(location=None, server=server):
    """Return the daily lag between collection and submission dates by location

    Arguments:
     :param location_id: (Somewhat optional). If not specified, return lag globally.
     :return: A pandas dataframe.
    """
    query = ''
    if location:
        query =  '&' + f'location_id={location}'
        
    raw_data = get_outbreak_data('genomics/collection-submission', query, collect_all=False)
    
    r = raw_data['results']
    
    for i in r: # for each seperate result
        values = tuple(i.values())
        
        if i == r[0]:
            df=pd.DataFrame({"date_collected": values[0], "date_submitted": values[1], "total_count": values[2]})
        else:
                newdf = pd.DataFrame({"date_collected": values[0], "date_submitted": values[1], "total_count": values[2]}) # append each df
                df = pd.concat([df, newdf], sort=False)
    return df
    

def wildcard_lineage(name, server=server):
    """Match lineage name using wildcards. 

    Arguments:
    :param name: (Required). A string. Supports wildcards. Must use '*' at end of string. (Example: b.1*, ba.2*)
    :return: A pandas dataframe."""
    
    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/lineage', query, collect_all=False)
    r = raw_data['results']
    
    for i in r: # for each separate result
        values = tuple(i.values())
        if i == r[0]: # follow new procedure as found for daily_lag
            df=pd.DataFrame({"name": values[0],
                  "total_count":values[1]}, index=[0])
        else:
                newdf = pd.DataFrame({"name": values[0],
                      "total_count":values[1]}, index=[0]) # append each df
                df = pd.concat([df, newdf], sort=False)
    return df
     


def wildcard_location(name, server=server):
    """Match location name using wildcards. 

    Arguments:
    :param name: (Required). A string. Must use * at end of string. Supports wildcards. (Example: united*)
    :return: A pandas dataframe."""
    
    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/location', query, collect_all=False)
    r = raw_data['results']
   
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"country": values[0], "country_id ": values[1],'id':values[2], "label":values[3],
                             "admin_level":values[4], "total_count":values[5]}, index = [0])
        else:
                newdf = pd.DataFrame({"country": values[0], "country_id ": values[1],'id':values[2], "label":values[3], 
                                      "admin_level":values[4], "total_count":values[5]}, index = [0]) # append each df
                df = pd.concat([df, newdf], sort=False)
    return df
     

def location_details(location, server=server):
    """Get location details using location ID.
     
    Arguments:
    :param location: A string. (Required).
    :return: Some pandas dataframes."""
   
    query = '' + '&' + f'id={location}'
    raw_data = get_outbreak_data('genomics/location-lookup', query, collect_all=False)
    data = {'Values' : raw_data['results']}
    df = pd.DataFrame(data) 
    return df

    
def wildcard_mutations(name, server=server):
    """Match mutations using wildcards.
    
     Arguments:
     :param name: (Required)  A string. Must use * at end of string. Supports wildcards. (Example: s:e484*)
     :return: A pandas dataframe."""

    query = '' + '&' + f'name={name}'
    raw_data = get_outbreak_data('genomics/mutations', query, collect_all=False)
    r = raw_data['results']
    
    for i in r: # for each seperate result
        values = tuple(i.values())
        if i == r[0]:
            df=pd.DataFrame({"name": values[0],
                  "total_count":values[1]}, index=[0])
        else:
                newdf = pd.DataFrame({"name": values[0],
                      "total_count":values[1]}, index=[0]) # append each df
                df = pd.concat([df, newdf], sort=False)
    return df

### Significance API enpoints: ###
    
def growth_rates(lineage, location='Global'):
    """Returns the growth rate score for a given lineage in a given location.
    
     Arguments:
     :param lineage: (Required)  A string. 
     :param location: (Required. Default: 'Global') A list or string. Separate multiple locations with ","
     :return: A pandas dataframe."""
    
    if isinstance(location, str):
        locations = location.replace(", " , "+OR+")
    elif isinstance(location, list):
             locations = '+OR+'.join(location)
    
    query = f'q=lineage:{lineage}+AND+location:{locations}'
    raw_data = get_outbreak_data('growth_rate/query', query, collect_all=False)
    df = pd.DataFrame(raw_data['hits'])
    
    return df


    
    



