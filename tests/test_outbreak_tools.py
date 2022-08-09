from outbreak_tools import plot_case_increase
import altair as alt


def _test_single_location():
    location = 'USA_US-CA'
    plot = plot_case_increase(location)
    assert(type(plot) == alt.vegalite.v4.api.Chart)


def test_plot_increase():
    """
    Tests the cases_by_location visualization tool in outbreak_tools
    """
    _test_single_location()

