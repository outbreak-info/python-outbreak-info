lineage_by_sub_admin(pango_lin, mutations, location, ndays=0, detected)
-----------------------------------------------------------------------

.. autofunction:: outbreak_data.lineage_by_sub_admin

Example usage::

    df = od.lineage_by_sub_admin('xbb.1.15', location='FRA')
    print(df)

.. code-block::
   :caption: Output:

           date              name          id          total_count  lineage_count  \
    0  2023-06-04                      FRA_FR-none          3              0   
    1  2023-05-31          Bretagne    FRA_FR-BT            2              0   
    2  2023-05-22             Corse    FRA_FR-CE            1              0   
    3  2023-05-30         Grand Est    FRA_FR-AO           68              0   
    4  2023-06-04         Normandie    FRA_FR-ND            2              0   
    5  2023-06-01         Occitanie    FRA_FR-LP            2              0   
    6  2023-05-30  Pays de la Loire    FRA_FR-PL           22              0   

       cum_total_count  cum_lineage_count  proportion  proportion_ci_lower  \
    0           406320                 10    0.000025         1.265376e-05   
    1            22070                  1    0.000045         4.888926e-06   
    2             2007                  0    0.000000         2.446305e-07   
    3            43954                  1    0.000023         2.454796e-06   
    4            19479                  0    0.000000         2.520808e-08   
    5            57933                  0    0.000000         8.475868e-09   
    6            24556                  0    0.000000         1.999632e-08   

       proportion_ci_upper  
    0             0.000044  
    1             0.000212  
    2             0.001251  
    3             0.000106  
    4             0.000129  
    5             0.000043  
    6             0.000102  
