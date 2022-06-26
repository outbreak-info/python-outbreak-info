import pandas as pd
import os
import sys
import altair as alt
data_path = os.path.realpath('outbreak_data')
sys.path.append(data_path)
import outbreak_common


def plot_increase(location):
    """
    Visualizes the confirmed increase in number of cases
    
    Arguments:
        location: Location as a string or list of location strings
        
    Returns:
        An interactive altair plot
    """
    data = outbreak_common.cases_by_location(location)

    return ...
