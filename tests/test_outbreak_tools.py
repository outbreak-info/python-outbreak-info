from outbreak_tools import outbreak_tools
import altair as alt


def _test_single_location():
    location = 'USA_US-CA'
    plot = outbreak_tools.plot_case_increase(location)

    assert(type(plot) == alt.vegalite.v4.api.Chart)


def test_plot_increase():
    """
    Tests the cases_by_location visualization tool in outbreak_tools
    """
    _test_single_location()

