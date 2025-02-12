growth_rates
-------------

.. autofunction:: outbreak_data.growth_rates

**Example Usage**

Get growth rate data for BA.2.86 on 2024-02-02 in the US::

    >>> df = outbreak_data.growth_rates('BA.2.86', 'USA')
    >>> df.loc['USA','BA.2.86','2024-02-02']
    >>> df

    G_7                                0.030113
    G_7_linear                         3.057071
    N_7                                0.000000
    N_prev_7                           1.000000
    Prevalence_7                       0.002365
    Prevalence_7_percentage            0.236476
    confidenceInterval20               1.044012
    confidenceInterval35               1.879221
    confidenceInterval5                0.250563
    confidenceInterval50               2.797951
    confidenceInterval65               3.883724
    confidenceInterval80               5.345340
    confidenceInterval95               8.185052
    deltaG_7                           0.040522
    deltaG_7_linear                    4.176047
    deltaN_7                        3108.000000
    deltaN_prev_7                      1.582951
    deltaPrevalence_7                  0.703224
    deltaPrevalence_7_percentage      70.322444
    invDeltaG_7                       24.678140
    snr                                0.732049
    Name: (USA, BA.2.86, 2024-02-02), dtype: float64

Get the prevalence percentage and 80% confidence intervals for BA.2 and BA.2.86::

    >>> df = outbreak_data.growth_rates('BA.2, BA.2.86' , 'USA')
    >>> df = df[[ 'Prevalence_7_percentage', 'confidenceInterval80']]
    >>> df

                          Prevalence_7_percentage  confidenceInterval80
    location lineage date                                                     
    USA      BA.2    2024-01-30                 0.184008              5.410016
                     2024-01-31                 0.180807              5.463835
                     2024-02-01                 0.178196              5.519133
                     2024-02-02                 0.176874              5.521128
                     2024-02-03                 0.175658              5.520665
    ...                                              ...                   ...
             BA.2.86 2024-03-07                 0.514831              6.592654
                     2024-03-08                 0.512352              6.565807
                     2024-03-09                 0.510145              6.595931
                     2024-03-10                 0.508168              6.524510
                     2024-03-11                 0.526594              6.380216

    [91 rows x 2 columns]
