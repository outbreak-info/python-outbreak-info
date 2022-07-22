import requests
import pandas as pd
import numpy as np

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def get_outbreak_data(endpoint, argstring, server=server, auth=auth):
    """
    Recieves raw data using outbreak API
       
    Arguments: 
        endpoint: directory in server the data is stored
        argstring: feature arguments to provide to API call
    
    Returns: 
        A request object containing the raw data
       
    """
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?q={argstring}', headers=auth)


def cases_by_location(location, server=server, auth=auth, pull_smoothed=0):
    """
    Loads data from a location; Use 'OR' between locations to get multiple.
#    Arguments:
#        location: A string
#    Returns:
#        A pandas dataframe
#    """
    if pull_smoothed == 0:
        confirmed='confirmed_numIncrease'
    elif pull_smoothed == 1:
        confirmed='confirmed_rolling'
    elif pull_smoothed == 2:
        confirmed='confirmed_rolling, confirmed_numIncrease'
    else:
        raise Exception("invalid parameter value for pull_smoothed!")
        
    raw_data = get_outbreak_data(covid19_endpoint,
                                                 f'location_id:{location}&sort=date&fields=date,{confirmed},admin1&{nopage}', server, auth)
    df=pd.DataFrame(raw_data.json()['hits'])
    refined_table=df.drop(columns=['_score', 'admin1'], axis=1)
    
    return refined_table

def page_cases_by_location(location, num_pages, server=server, auth=auth, covid19_endpoint=covid19_endpoint):
    """
    Loads data from a location; Use 'OR' between locations to get multiple.
    Uses a paging mechanism.

    Arguments:
        location: A string

    Returns:
        A pandas dataframe

    """
    auth = {'Authorization': str(auth)}                     

    scroll_id = raw_data.json()['_scroll_id']
    scroll_df = pd.DataFrame(columns=pd.Series(raw_data.json()['hits'][0]).index)

    fetching_page = '&fetch_all=True&page='
    curr_page = 1
    while curr_page <= num_pages:
        # individual request df
        data = pd.DataFrame(raw_data.json()['hits'])
        scroll_df = scroll_df.append(data, ignore_index=True)

        page = fetching_page + str(curr_page)
        to_scroll = 'scroll_id=' + scroll_id + page
        raw_data = requests.get(f'https://{server}/{covid19_endpoint}?{to_scroll}', headers=auth)
        curr_page += 1

    # applying datetime to dates column and sorting in ascending
    scroll_df['date'] = scroll_df['date'].apply(lambda x: pd.to_datetime(x))
    scroll_df = scroll_df.sort_values(by='date', ascending=True)
    scroll_df.reset_index(drop=True, inplace=True)
    return scroll_df
