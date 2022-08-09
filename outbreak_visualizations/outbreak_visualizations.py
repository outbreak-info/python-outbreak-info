import altair as alt
from outbreak_data import outbreak_data
import pandas as pd


def plot_cases_by_location(location, smoothed=True, past_num_days = None):
    """
    Visualizes the confirmed increase in number of cases

    :param location: Location as a string or list of location strings
    :param smoothed: Default True plots rolling averaged data
    :param past_num_days: If not None, filters data to past x num days.
    :return: An interactive altair plot
    """
    smooth = 1
    y_col = 'confirmed_rolling:Q'
    plot_title = 'Confirmed Cases (7-Day Rolling)'
    if not smoothed:
        smooth = 0
        y_col = 'confirmed_numIncrease:Q'
        plot_title = 'SARS-CoV-2 Increase'
    data = outbreak_data.cases_by_location(location, pull_smoothed=smooth)
    data['date'] = data['date'].apply(pd.to_datetime)
    if past_num_days != None:
        if isinstance(past_num_days, int) & (past_num_days > 0):
            today = pd.Timestamp.today()
            delta = pd.Timedelta(days=past_num_days)
            data = data.where(data['date'].apply(lambda x: x > (today - delta))).dropna(how='all')
    # base feature viz // amount of new covid cases
    base = alt.Chart(data, title=plot_title).mark_line().encode(
        x='date:T',
        y=y_col,
        color='admin1:N'
    )

    return base