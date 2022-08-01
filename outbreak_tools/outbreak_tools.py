import altair as alt
from outbreak_data import outbreak_data


def id_lookup(location):
    """
    Helps find location ID for use with outbreak_data.py
    :param location:
    :return: location_id
    """
    return ...


def plot_increase(location, smoothed=True):
    """
    Visualizes the confirmed increase in number of cases

    :param location: Location as a string or list of location strings
    :param smoothed: Default True plots rolling averaged data
    :return: An interactive altair plot
    """
    smooth = 1
    y_col = 'confirmed_rolling:Q'
    plot_title = 'SARS-CoV-2 7-Day Rolling Increase'
    if not smoothed:
        smooth = 0
        y_col = 'confirmed_numIncrease:Q'
        plot_title = 'SARS-CoV-2 Increase'
    data = outbreak_data.cases_by_location(location, pull_smoothed=smooth)
    # base feature viz // amount of new covid cases
    base = alt.Chart(data, title=plot_title).mark_line().encode(
        x='date:T',
        y=y_col,
        color='admin1:N'
    ).interactive()

    return base




