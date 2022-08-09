from outbreak_visualizations import outbreak_visualizations
import altair as alt


def _test_single_location():
    location = 'USA_US-CA'
    expected_loc_name = 'California'
    plot = outbreak_visualizations.plot_cases_by_location(location)
    assert type(plot) == alt.vegalite.v4.api.Chart, 'Visualization not returning correct format'
    plotted_loc = plot.data.admin1.unique()[0]
    assert plotted_loc == expected_loc_name, 'Visualization not plotting correct location'

def _test_multiple_locations():
    locations = ['USA_US-CA', 'USA_US-OR', 'USA_US-WA', 'USA_US-NV']
    plot = outbreak_visualizations.plot_cases_by_location(locations)
    assert type(plot) == alt.vegalite.v4.api.Chart, 'Visualization not returning correct format'
    plotted_locs = plot.data.admin1.unique()
    assert len(plotted_locs) == len(locations), 'Visualization not plotting all locations'

def test_plot_cases_by_location():
    """
    Tests the cases_by_location visualization tool in outbreak_tools
    """
    _test_single_location()
    _test_multiple_locations()

