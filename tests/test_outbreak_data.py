from outbreak_data import outbreak_data
import pandas as pd

test_server = 'test.outbreak.info'


def _test_missing_auth():
    missing_auth = ''
    location = 'USA_US-CA'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1'
                                          f'&{outbreak_data.nopage}', server=test_server, auth_key=missing_auth,
                                          collect_all=True)
    assert isinstance(out, type(None)), f'get_outbreak_data returning data despite authentication error'


def _test_malformed_auth():
    malformed_auth = 'Bearer qfsb1pkhk6138ly1rfk1cbgityi9b73boygqe5r39sxpmz3djtu1qkdqtj2wu6ft'
    location = 'USA_US-CA'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1'
                                          f'&{outbreak_data.nopage}', server=test_server, auth_key=malformed_auth,
                                          collect_all=True)

    assert isinstance(out, type(None)), f'get_outbreak_data not returning correct data for {location}'


def test_outbreak_auth():
    _test_missing_auth()
    _test_malformed_auth()


def _test_get_location():
    """
    Test the ability of get data to return a location's case data within a
    pandas dataframe
    """
    location = 'AUS_SouthAustralia'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{location}&sort=date&fields=date,confirmed_numIncrease,admin1'
                                          f'&{outbreak_data.nopage}', server=test_server, collect_all=True)
    df = pd.DataFrame(out['hits'])
    assert df.admin1.unique()[0] == 'South Australia', f'get_outbreak_data not returning correct data for {location}'


def _test_get_multiple_locations():
    """
    Test the ability of get data to return multiple locations.
    """
    location = ['AUS_SouthAustralia', 'USA_US-NY', 'USA_US-TX']
    locations = '(' + ' OR '.join(location) + ')'
    out = outbreak_data.get_outbreak_data('covid19/query',
                                          f'q=location_id:{locations}'
                                          f'&sort=date&fields=date,confirmed_numIncrease,admin1&{outbreak_data.nopage}',
                                          server=test_server, collect_all=True)
    df = pd.DataFrame(out['hits'])
    assert len(df.admin1.unique()) == len(location), f'get_outbreak_data returning incorrect number of locations, ' \
                                                     f'expected {len(location)}'
    location_names = sorted(['California', 'New York', 'Texas'])
    output_names = sorted(df.admin1.unique())
    for i in range(len(location_names)):
        assert location_names[i] == output_names[i], f'output locations {location_names} do not correspond to input' \
                                                     f' codes: {location}'


def test_get_outbreak_data():
    """
    Main test
    """
    _test_get_location()
    # test_get_multiple_locations()


def _test_cases_single_location():
    location = 'USA_US-CA'
    out = outbreak_data.cases_by_location(location)
    assert out.admin1.unique()[0] == 'California', f'cases_by_location not returning correct data for {location}'


def _test_cases_multiple_location():
    locations = ['USA_US-CA', 'USA_US-NY', 'USA_US-TX']
    out = outbreak_data.cases_by_location(locations)
    assert len(out.admin1.unique()) == len(locations), f'cases_by_location returning an incorrect number of locations,' \
                                                       f' expected {len(locations)}'
    location_names = sorted(['California', 'New York', 'Texas'])
    output_names = sorted(out.admin1.unique())
    for i in range(len(location_names)):
        assert location_names[i] == output_names[i], f'output locations {location_names} do not correspond to input' \
                                                     f' codes: {locations}'


def test_cases_by_location():
    """
    Main test
    """
    _test_cases_single_location()
    _test_cases_multiple_location()
