"""
Script to update the .csv files backing the testing suite.
"""
import os
import sys
import requests
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from outbreak_data import outbreak_data

test_server = 'test.outbreak.info'
null_server = 'null.outbreak.info'


def update_all_test_lineage_mutations():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'lineage_mutations.csv')
    val1 =  outbreak_data.lineage_mutations('BA.2 OR B.1.1.7', server=test_server)
    val1.to_csv(save_file)

def update_mutations_by_lineage():
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'mut_across_lin_test.csv')
    val1 = outbreak_data.mutations_by_lineage('orf1a:g1307s', 'USA', server=test_server)
    val1.to_csv(save_file)

def update_global_prevalence():
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'global_prev_test.csv')
    val1 = outbreak_data.global_prevalence('ba.2', 'orf1a:t842i', server=test_server)
    val1.to_csv(save_file)

def update_all_sequence_counts():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'sequence_counts.csv')
    val1 =  outbreak_data.sequence_counts('USA_US-CA', server=test_server)
    val1.to_csv(save_file)

# def update_all_prevalence_by_location():
#     #test one
#     save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'prevalence_by_location.csv')
#     val1 = outbreak_data.prevalence_by_location('USA_US-NY', startswith='b.1', server=test_server)
#     val1.to_csv(save_file)

def update_all_daily_prev():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'daily_prev.csv')
    val1 = outbreak_data.daily_prev('BA.2', server=test_server)
    val1.to_csv(save_file)

def update_all_lineage_by_sub_admin():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'sub_admin.csv')
    val1 = outbreak_data.lineage_by_sub_admin('XBB.1.5', location='USA', server=test_server)
    val1.to_csv(save_file)
    
def update_all_collection_date():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'collection_date.csv')
    val1 = outbreak_data.collection_date('BA.1', server=test_server)
    val1.to_csv(save_file)
    
def update_all_submission_date():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'submission_date.csv')
    val1 = outbreak_data.submission_date('BA.1', server=test_server)
    val1.to_csv(save_file)
    
def update_all_mutation_details():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'mutation_details.csv')
    val1 = outbreak_data.mutation_details('orf1a:t842i', server=test_server)
    val1.to_csv(save_file)
    
def update_all_daily_lag():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'daily_lag.csv')
    val1 = outbreak_data.daily_lag('LUX', server=test_server)
    val1.to_csv(save_file)

def update_all_wildcard_lineage():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_lineage.csv')
    val1 = outbreak_data.wildcard_lineage('b.1*', server=test_server)
    val1.to_csv(save_file)
    
def update_all_wildcard_location():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_location.csv')
    val1 = outbreak_data.wildcard_location('united*', server=test_server)
    val1.to_csv(save_file)
    
def update_all_location_details():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'location_details.csv')
    val1 = outbreak_data.location_details('CHN', server=test_server)
    val1.to_csv(save_file)
    
def update_all_wildcard_mutations():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'wildcard_mutations.csv')
    val1 = outbreak_data.wildcard_mutations('s:e484*', server=test_server)
    val1.to_csv(save_file)


def main():
    update_all_test_lineage_mutations()
    update_mutations_by_lineage()
    update_global_prevalence()
    update_all_sequence_counts()
    # update_all_prevalence_by_location()
    update_all_daily_prev()
    update_all_lineage_by_sub_admin()
    update_all_collection_date()
    update_all_submission_date()
    update_all_mutation_details()
    update_all_daily_lag()
    update_all_wildcard_lineage()
    update_all_wildcard_location()
    update_all_location_details()
    update_all_wildcard_mutations()
    
    


if __name__ == "__main__":
    main()
