import altair as alt
from outbreak_data import outbreak_data
import pandas as pd


def id_lookup(locations):
    """
    Helps find location ID for use with outbreak_data.py
    Requires integration with get_outbreak_data
    :param locations:
    :return: location_id
    """
    locIds_of_interest=[]
    locIds_not_found=[]
    for i in locations:
        locId_arg = "name=" + i
        results = outbreak_data.get_outbreak_data('genomics/location', locId_arg)
        hits = None
        if(len(results) >= 1):
            hits = results
        if(len(hits) == 0):
            locIds_not_found.extend([i])
        else:
            df = pd.DataFrame(hits['results'])
            if (df.shape[0]==1):
                locIds_of_interest.extend([df.id.unique()[0]])
            else:
                locIds_not_found.extend([i])

        if (len(locIds_of_interest)==len(locations)):
            return locIds_of_interest
        if (len(locIds_of_interest)!=len(locations)):
            locations_not_found=[]
            for i in locIds_not_found:
                locs=''.join(['*', i, '*'])
                locations_not_found.extend([locs])
            for i in range(0, len(locations_not_found)):
                locId = "name=" + locations_not_found[i]
                results = outbreak_data.get_outbreak_data('genomics/location', locId)
                hits = pd.DataFrame()
                if(len(results) >= 1):
                    hits = pd.DataFrame(results['results'])
                if(hits.shape[0] == 0):
                    next
                else:
                    df.admin_level.replace(-1, "World Bank Region", inplace=True)
                    df.admin_level.replace(0, "country", inplace=True)
                    df.admin_level.replace(1, "state/province", inplace=True)
                    df.admin_level.replace(1.5, "metropolitan area", inplace=True)
                    df.admin_level.replace(2, "county", inplace=True)
                    df['full'] = df.label + ' ' + " (" + ' ' + df.admin_level + ' ' + ")"
                    for i in df.full:
                        print(i)
                        print("\n")
                        loc_sel = input("Is this a location of interest? (Y/N): ")
                        if ((loc_sel == "Y")|(loc_sel == "y")):
                            locIds_of_interest.extend(df.id[df.full==i])
                            break
                        if ((loc_sel != "Y")&(loc_sel != "y")&(loc_sel != "N")&(loc_sel != "n")):
                            print("Expected input is Y or N\n\n")
                            print('\n')
                            print(i)
                            loc_sel = input("Is this a location of interest? (Y/N): ")
                            if ((loc_sel == "Y")|(loc_sel == "y")):
                                locIds_of_interest.extend(df.id[df.full==i])
                                break
    return locIds_of_interest


def plot_case_increase(location, smoothed=True):
    """
    Visualizes the confirmed increase in number of cases

    :param location: Location as a string or list of location strings
    :param smoothed: Default True plots rolling averaged data
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
    data = data.where(data['date'].apply(lambda x: x > pd.Timestamp(year=2022, month =5, day=26))).dropna(how='all')
    # base feature viz // amount of new covid cases
    base = alt.Chart(data, title=plot_title).mark_line().encode(
        x='date:T',
        y=y_col,
        color='admin1:N'
    )

    return base