import altair as alt
from outbreak_data import outbreak_data


server = 'api.outbreak.info'  # or 'dev.outbreak.info'
auth = 'Bearer 0ed52bbfb6c79d1fd8e9c6f267f9b6311c885a4c4c6f037d6ab7b3a40d586ad0'  # keep this private!
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

