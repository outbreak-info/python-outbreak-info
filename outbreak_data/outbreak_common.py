import requests
import pandas as pd
import numpy as np

server = 'api.outbreak.info' # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0' # keep this private!
nopage = 'fetch_all=true&page=0' # worth verifying that this works with newer ES versions as well

def get_outbreak_data(endpoint, argstring, server=server, auth=auth):
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?q={argstring}', headers=auth)

def cases_by_location(location, server=server, auth=auth):
    raw_data =  get_outbreak_data('covid19/query',
        f'location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}',
        server, auth )
    return pd.DataFrame(raw_data.json()['hits'])

def get_multiple_locations(locations):
    out = []
    for state in locations:
        data = cases_by_location(state)
        out.append(data)
    return pd.concat(out)

def rolling_average(data, num_days):
    if len(data) <=  num_days:
        print('Not enough data')
        return None
    else:
        output_rolled = np.convolve(data, np.ones(num_days)/num_days, mode="valid")
        pads = np.array([0] * (num_days - 1))
        return np.concatenate((pads, output_rolled))