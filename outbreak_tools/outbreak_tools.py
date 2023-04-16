from outbreak_data import outbreak_data
import pandas as pd
import re
import warnings


def id_lookup(locations, max_results = 10, table = False):
    """
    Helps find location ID for use with outbreak_data.py
    Requires integration with get_outbreak_data
    :param locations: A string or list of location names
    :param max_results: Int, of how many results to return
    :param table: If True, returns all results as pandas DataFrame
    :return: location_id
    """
    warnings.filterwarnings("ignore", message='Warning!: Data has "results" but length of data is 0')
    #setting max_colwidth for showing full-name completely in table
    pd.set_option("max_colwidth", 300)
    locIds_of_interest=[]
    locIds_not_found=[]
    locations_not_found=[]
    if isinstance(locations, str):
        locations = [locations]
    #first pass of the query tries every location name as-is & collects malformed queries
    for i in locations:
        locId_arg = "name=" + i
        results = outbreak_data.get_outbreak_data('genomics/location', locId_arg)
        if results != None:
            if (len(results) == 0):
                locIds_not_found.extend([i])
            else:
                df = pd.DataFrame(results['results'])
                #print(df.columns)
                if (df.shape[0]==1):
                    locIds_of_interest.extend([df.id.unique()[0]])
                else:
                    locIds_not_found.extend([i])
        #everything matches up
        if (len(locIds_of_interest)==len(locations)):
            return locIds_of_interest
        #any locations not found require further investigation (*name* must be a catch-all?)
        if (len(locIds_of_interest)!=len(locations)):
            not_found=[]
            for i in locIds_not_found:
                locs=''.join(['*', i, '*'])
                not_found.extend([locs])
            locations_not_found = not_found
    all_hits = None
    #using genomic endpoint to parse location names and corrects malformed queries
    for i in range(0, len(locations_not_found)):
        locId = "name=" + locations_not_found[i]
        results = outbreak_data.get_outbreak_data('genomics/location', locId)
        hits = pd.DataFrame()
        if(len(results) >= 1):
            hits = pd.DataFrame(results['results'])
        if(hits.shape[0] == 0):
            next
        else:
            #replacing code with meaning
            hits.admin_level.replace(-1, "World Bank Region", inplace=True)
            hits.admin_level.replace(0, "country", inplace=True)
            hits.admin_level.replace(1, "state/province", inplace=True)
            hits.admin_level.replace(1.5, "metropolitan area", inplace=True)
            hits.admin_level.replace(2, "county", inplace=True)
            hits['full'] = hits.label + ' ' + " (" + ' ' + hits.admin_level + ' ' + ")"
            hits = hits[:max_results]
            hits.index= pd.MultiIndex.from_arrays([[locations_not_found[i].strip('*')] * len(hits.index)
                                                      ,list(hits.index)], names=['Query', 'Index'])
            if isinstance(all_hits, pd.core.frame.DataFrame):
                all_hits = all_hits.append(hits)
            else:
                all_hits = hits.copy()
            if not table:
                # ask questions about ambiguous names (one-to-many)
                print("\n")
                display(hits['full'])
                print('Int values must be entered in comma seperated format.')
                loc_sel = input("Enter the indices of locations of interest in dataframe above: ")
                if loc_sel == '':
                    raise ValueError('Input string is empty, enter single or multiple int comma seperated value/s before submitting.')
                input_locs = list(loc_sel.split(','))
                for i in range(len(input_locs)):
                    val = re.search(r' *[0-9]+', input_locs[i])
                    if (isinstance(val, re.Match)):
                        if (val.group() != ''):
                            val = int(val.group())
                            input_locs[i] = val
                all_int = all([isinstance(x, int) for x in input_locs])
                if all_int:
                    locIds_of_interest.extend(hits.iloc[input_locs, :].id)
                else:
                    print("Input entries are all not int. Please try again.")
                    print('\n')
                    display(hits['full'])
                    loc_sel = input("Enter the indices of locations of interest in dataframe above: ")
                    if loc_sel == '':
                        raise ValueError('Input string is empty, enter single or multiple int comma seperated value/s before submitting.')
                    input_locs = list(loc_sel.split(','))
                    for i in range(len(input_locs)):
                        val = re.search(r' *[0-9]+', input_locs[i])
                        if (isinstance(val, re.Match)):
                            if (val.group() != ''):
                                val = int(val.group())
                                input_locs[i] = val
                    all_int = all([isinstance(x, int) for x in input_locs])
                    if all_int:
                        locIds_of_interest.extend(hits.iloc[input_locs, :].id)
                print('\n')
    if table:
        #necessary identification
        return all_hits.loc[:, ['id', 'label', 'admin_level']]
    return locIds_of_interest