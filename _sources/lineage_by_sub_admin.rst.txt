lineage_by_sub_admin
---------------------------------

.. autofunction:: outbreak_data.lineage_by_sub_admin

**Example Usage**

Get the number of lineages sequenced and recorded in each province in France::

    >>> df = od.lineage_by_sub_admin('xbb.1.15', location='FRA')
    >>> df
                                    date           id  total_count  \
    name             query                                            
                     xbb.1.15  2024-05-13  FRA_FR-None            1   
    Bretagne         xbb.1.15  2024-04-25    FRA_FR-BT            1   
    Corse            xbb.1.15  2024-04-29    FRA_FR-CE            1   
    Grand Est        xbb.1.15  2024-04-15    FRA_FR-AO            2   
    Normandie        xbb.1.15  2024-04-08    FRA_FR-ND            2   
    Occitanie        xbb.1.15  2024-05-06    FRA_FR-LP            3   
    Pays de la Loire xbb.1.15  2024-04-02    FRA_FR-PL            5   

                               lineage_count  cum_total_count  cum_lineage_count  \
    name             query                                                         
                     xbb.1.15              0             4504                  0   
    Bretagne         xbb.1.15              0              398                  0   
    Corse            xbb.1.15              0               51                  0   
    Grand Est        xbb.1.15              0              784                  0   
    Normandie        xbb.1.15              0              195                  0   
    Occitanie        xbb.1.15              0              618                  0   
    Pays de la Loire xbb.1.15              0              229                  0   

                               proportion  proportion_ci_lower  \
    name             query                                       
                     xbb.1.15         0.0         1.090158e-07   
    Bretagne         xbb.1.15         0.0         1.232980e-06   
    Corse            xbb.1.15         0.0         9.581002e-06   
    Grand Est        xbb.1.15         0.0         6.261197e-07   
    Normandie        xbb.1.15         0.0         2.514896e-06   
    Occitanie        xbb.1.15         0.0         7.942326e-07   
    Pays de la Loire xbb.1.15         0.0         2.141914e-06   

                               proportion_ci_upper  
    name             query                          
                     xbb.1.15             0.000558  
    Bretagne         xbb.1.15             0.006288  
    Corse            xbb.1.15             0.047830  
    Grand Est        xbb.1.15             0.003198  
    Normandie        xbb.1.15             0.012783  
    Occitanie        xbb.1.15             0.004055  
    Pays de la Loire xbb.1.15             0.010897

