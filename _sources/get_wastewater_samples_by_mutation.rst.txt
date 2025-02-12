get_wastewater_samples_by_mutation
------------------------------------

.. autofunction:: outbreak_data.get_wastewater_samples_by_mutation

**Example Usage**

Find wastewater samples with A --> G base mutations at position 1003::

    >>> outbreak_data.get_wastewater_samples_by_mutation(site=1003, alt_base='G', server='dev.outbreak.info')

                       alt_base  depth  prevalence ref_base  site sra_accession
    mutation                                                                    
    1003 AND alt_base:G        G     51    0.038088        A  1003   SRR21864715
    1003 AND alt_base:G        G     37    0.016364        A  1003   SRR26898771
    1003 AND alt_base:G        G  17489    0.267682        A  1003   SRR22275905
    1003 AND alt_base:G        G   2708    0.024436        A  1003   SRR27050417
    1003 AND alt_base:G        G   1398    0.677654        A  1003   SRR26979184
    1003 AND alt_base:G        G     51    0.015450        A  1003   SRR21662569
    1003 AND alt_base:G        G  17049    0.355165        A  1003   SRR24899723
    1003 AND alt_base:G        G    119    0.010776        A  1003   SRR21492603
    1003 AND alt_base:G        G    145    0.018189        A  1003   SRR26111437
    1003 AND alt_base:G        G    254    0.072884        A  1003   SRR24837595
    1003 AND alt_base:G        G     20    0.256410        A  1003   SRR26776578
    ...		           ...	       ...	       ...       ...

    [45 rows x 6 columns]
