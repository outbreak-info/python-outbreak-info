prevalence_by_location(pango_lin, location, mutations=None, datemin=None, datemax=None, cumulative=None, lineage_crumbs=False)
-------------------------------------------------------------------------------------------------------------------------------

.. autofunction:: outbreak_data.prevalence_by_location

Example usage:

1. Get the daily prevalence of lineage 'BA.2' in India since first detection::

    df1 = od.daily_prev('ba.2', "IND")
    print(df1)

.. code-block::
   :caption: Output

                date  total_count  lineage_count  total_count_rolling  \
    0     2020-08-01           39              1            29.000000   
    1     2020-08-02          100              0            41.285714   
    2     2020-08-03           38              0            42.000000   
    3     2020-08-04           20              0            42.285714   
    4     2020-08-05           26              0            36.000000   
    ...          ...          ...            ...                  ...   
    1017  2023-05-15            2              0             5.857143   
    1018  2023-05-16            3              0             5.142857   
    1019  2023-05-17            3              0             3.285714   
    1020  2023-05-18            2              0             3.142857   
    1021  2023-05-20            1              0             2.000000   

          lineage_count_rolling  proportion  proportion_ci_lower  \
    0                  0.142857    0.004926             0.000017   
    1                  0.142857    0.003460             0.000012   
    2                  0.142857    0.003401             0.000012   
    3                  0.142857    0.003378             0.000012   
    4                  0.142857    0.003968             0.000014   
    ...                     ...         ...                  ...   
    1017               0.000000    0.000000             0.000078   
    1018               0.000000    0.000000             0.000093   
    1019               0.000000    0.000000             0.000151   
    1020               0.000000    0.000000             0.000151   
    1021               0.000000    0.000000             0.000217   

          proportion_ci_upper  
    0                0.082286  
    1                0.059076  
    2                0.057719  
    3                0.057719  
    4                0.066944  
    ...                   ...  
    1017             0.330389  
    1018             0.379377  
    1019             0.535583  
    1020             0.535583  
    1021             0.666822

2. Get a cumulative summary of information regarding 'BA.2' in India::

    df2 = od.daily_prev('ba.2', "IND", cumulative = True)
    print(df2)

.. code-block::
   :caption: Output

                           Values
    first_detected     2020-08-01
    global_prevalence    0.109641
    last_detected      2023-04-26
    lineage_count           25561
    total_count            233134  

