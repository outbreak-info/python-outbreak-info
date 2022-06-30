import requests
import pandas as pd

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def get_outbreak_data(endpoint, collect_all, argstring, server=server, auth=auth):
    """
    Receives raw data using outbreak API

    :param endpoint: directory in server the data is stored
    :param argstring: feature arguments to provide to API call
    :param collect_all: if True, returns all data.
    :return: A request object containing the raw data
    """
    auth = {'Authorization': str(auth)}

    def api_call(scrolling, argstring):
        if scrolling:
            return requests.get(f'https://{server}/{endpoint}?{argstring}', headers=auth)
        else:
            return requests.get(f'https://{server}/{endpoint}?q={argstring}', headers=auth)

    def page_data(data_in):
        """
        Used as a helper function to page through results and return more data.
        :param data_in: Initial request containing the args
        :param server: Used to call which server in the API.
        :param auth: Used as a header in call to the API.
        :param endpoint: Used to specify the endpoint the covid19 data is stored.
        :return: Pandas Dataframe
        """
        scroll_id = data_in.json()['_scroll_id']
        data_out = pd.DataFrame(columns=pd.Series(data_in.json()['hits'][0]).index)

        fetching_page = '&fetch_all=True&page='
        curr_page = 0
        while 'success' not in data_in.json().keys():
            # individual request df
            data = pd.DataFrame(data_in.json()['hits'])
            data_out = data_out.append(data, ignore_index=True)

            page = fetching_page + str(curr_page)
            to_scroll = 'scroll_id=' + scroll_id + page
            data_in = api_call(True, to_scroll)

        # applying datetime to dates column and sorting in ascending
        data_out['date'] = data_out['date'].apply(lambda x: pd.to_datetime(x))
        data_out = data_out.sort_values(by='date', ascending=True)
        data_out.reset_index(drop=True, inplace=True)
        return data_out

    data_origin = api_call(False, argstring)
    if collect_all:
        return page_data(data_origin)
    else:
        return data_origin


def cases_by_location(location, server=server, auth=auth):
    """
    Loads data from a location; Use 'OR' between locations to get multiple.

    :param location: A string
    :return: A pandas dataframe

    """
    return get_outbreak_data(covid19_endpoint, True, f'location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}')
