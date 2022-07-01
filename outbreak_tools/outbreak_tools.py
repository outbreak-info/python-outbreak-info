import sys
sys.path.insert(0, 'pathname/outbreak_data') 

""" Import outbreak_data.py from directory location """

import altair as alt
import pandas as pd
import outbreak_data

server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = ***REMOVED***  # keep this private!
nopage = 'fetch_all=true&page=0'  # worth verifying that this works with newer ES versions as well
covid19_endpoint = 'covid19/query'


def plot_increase(location, all_data, num_pages = None):
    """
    Visualizes the confirmed increase in number of cases
    
    Arguments:
        location: Location as a string or list of location strings
        num_pages: Amount of pages (1000 obs/page) of data to use
        all_data: Whether to use all data or num_pages
    Returns:
        An interactive altair plot
    """
    data = outbreak_data.cases_by_location(location, all_data, num_pages)
    # base feature viz // amount of new covid cases
    base = alt.Chart(data).mark_line().encode(
        x='date:T',
        y='confirmed_numIncrease:Q',
        color='admin1:N'
    ).interactive()
    
    return base

def cases_by_location(location, collect_all=True, num_pages=None, server=server, auth=auth):
    """
    Loads data from a location; Use 'OR' between locations to get multiple.

    Arguments:
        :param location: A string: iso3
        :param num_pages: For every value >= 0, returns 1000 obs. (paging)
        :param collect_all: If true returns all pages
    Returns:
        A pandas dataframe

    """
    assert(type(collect_all) == bool)
    raw_data = outbreak_data.get_outbreak_data('covid19/query',
                                               f'location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1&{nopage}',
                                               server, auth)
    if collect_all:
        assert(num_pages is None)
        return outbreak_data.page_data(raw_data, True)
    else:
        assert(num_pages is not None)
        assert(type(num_pages) == int)
        assert(num_pages >= 0)

        if num_pages == 0:
            return pd.DataFrame(raw_data.json()['hits'])
        elif num_pages > 0:
            return outbreak_data.page_data(raw_data, collect_all, num_pages)

def prevalence_by_location(location, pango_lin = None, startswith=None, server=server, auth=auth):
   """
   Loads prevalence data from a location

   Arguments:
       :param location: A string
       :param num_pages: For every value >= 0, returns 1000 obs. (paging)
       :param pango_lin: A string; loads data for a specifc lineage
       :param startswith: A string; loads data for all lineages beginning with first letter(s) of name
   Returns:
       A pandas dataframe
   """
   raw_data = outbreak_data.get_prevalence_by_location('genomics/prevalence-by-location-all-lineages', f'location_id={location}&sort=date&ndays=2048&nday_threshold=0&other_threshold=0').json()['results']
   lins = pd.DataFrame(raw_data)
    
   if startswith is not None:
      search_all = startswith
      return lins.loc[lins['lineage'].str.startswith(search_all)]
   else:
      return lins.loc[lins['lineage']== pango_lin]
  
