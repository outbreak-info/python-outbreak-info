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
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_one.csv')
    val1 =  outbreak_data.lineage_mutations('BA.2', server=test_server)
    val1.to_csv(save_file)

    #test two
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_two.csv')
    val1 = outbreak_data.lineage_mutations('BA.2 OR B.1.1.7', server=test_server)
    val1.to_csv(save_file)

    #test three
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_three.csv')
    val1 = outbreak_data.lineage_mutations('BA.2, B.1.1.7', server=test_server)
    val1.to_csv(save_file)

    #test four 
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'test_four.csv')
    val1 = outbreak_data.lineage_mutations('BA.2','s:p681h', server=test_server)
    val1.to_csv(save_file)

def update_mutations_by_lineage():
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'mut_across_lin_test.csv')
    val1 = outbreak_data.mutations_by_lineage('orf1a:g1307s', 'USA', server=test_server)
    val1.to_csv(save_file)

def update_global_prevalence():
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'global_prev_test.csv')
    val1 = outbreak_data.global_prevalence('ba.2', 'orf1a:t842i', server=test_server)
    val1.to_csv(save_file)


def update_all_prevalence_by_location():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'prev1.csv')
    val1 = outbreak_data.prevalence_by_location('USA_US-CO', server=test_server)
    val1.to_csv(save_file)

    #test two
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'prev2.csv')
    val1 = outbreak_data.prevalence_by_location('USA_US-NY', startswith='b.1', server=test_server)
    val1.to_csv(save_file)

def update_all_sequence_counts():
    #test one
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count1.csv')
    val1 = outbreak_data.sequence_counts(server=test_server)
    val1.to_csv(save_file)

    #test two
    save_file = os.path.join(os.path.dirname(__file__),'test_data', 'seq_count2.csv')
    val1 = outbreak_data.sequence_counts('USA_US-CA', server=test_server)
    val1.to_csv(save_file)

    #test three
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count3.csv')
    val1 = outbreak_data.sequence_counts('USA', cumulative=True, server=test_server)
    val1.to_csv(save_file)

    #test four
    save_file = os.path.join(os.path.dirname(__file__), 'test_data', 'seq_count4.csv')
    val1 = outbreak_data.sequence_counts('USA', True, True, server=test_server)
    val1.to_csv(save_file)

def main():
    update_global_prevalence()
    update_mutations_by_lineage()
    update_all_test_lineage_mutations()
    update_all_prevalence_by_location()
    update_all_sequence_counts()


if __name__ == "__main__":
    main()
