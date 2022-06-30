import altair as alt
from outbreak_data import outbreak_data


def plot_increase(location):
    """
    Visualizes the confirmed increase in number of cases

    :param location: Location as a string or list of location strings
    :param num_pages: Amount of pages (1000 obs/page) of data to use
    :param all_data: Whether to use all data or num_pages
    :return: An interactive altair plot
    """
    data = outbreak_data.cases_by_location(location, True)
    # base feature viz // amount of new covid cases
    base = alt.Chart(data).mark_line().encode(
        x='date:T',
        y='confirmed_numIncrease:Q',
        color='admin1:N'
    ).interactive()

    return base
