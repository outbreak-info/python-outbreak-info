import requests
import pandas as pd

server = 'api.outbreak.info' # or 'dev.outbreak.info'
auth = ***REMOVED*** # keep this private!
nopage = 'fetch_all=true&page=0' # worth verifying that this works with newer ES versions as well

def get_outbreak_data(endpoint, argstring, server=server, auth=auth):
    auth = {'Authorization': str(auth)}
    return requests.get(f'https://{server}/{endpoint}?q={argstring}', headers=auth)

def cases_by_location(location, server=server, auth=auth):
    raw_data =  get_outbreak_data('covid19/query',
        f'location_id:{location}&sort=date&fields=date,confirmed_numIncrease&{nopage}',
        server, auth )
    return pd.DataFrame(raw_data.json()['hits'])
