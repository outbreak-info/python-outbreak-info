import os
import sys
data_path = os.path.abspath('../outbreak_data')
sys.path.append(data_path)
import outbreak_common
import pandas as pd
# TODO: This could be a prompt
state_list = ['USA_US-CO', 'USA_US-WA', 'USA_US-MN', 'USA_US-LA']
states = outbreak_common.get_multiple_locations(state_list)
# TODO: This could also be a prompt
states.to_csv('camping_states.csv', index = False)