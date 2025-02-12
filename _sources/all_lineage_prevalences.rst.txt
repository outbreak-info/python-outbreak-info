all_lineage_prevalences
---------------------------------------------

.. autofunction:: outbreak_data.all_lineage_prevalences


Example usage::
    
    #Find the prevalence all lineages in Argentina that begin with 'xbb.1'  
    df = od.prevalence_by_location("ARG", startswith = 'xbb.1')
    print(df)

.. code-block::
   :caption: Output

                date  total_count  lineage_count  lineage  prevalence  \
    1454  2022-10-12            3              1    xbb.1    0.333333   
    1455  2022-10-13            0              0    xbb.1    0.000000   
    1456  2022-10-14            0              0    xbb.1    0.000000   
    1457  2022-10-15            0              0    xbb.1    0.000000   
    1458  2022-10-16            0              0    xbb.1    0.000000   
    ...          ...          ...            ...      ...         ...   
    1673  2023-03-17            0              0  xbb.1.5    0.000000   
    1674  2023-03-18            0              0  xbb.1.5    0.000000   
    1675  2023-03-19            0              0  xbb.1.5    0.000000   
    1676  2023-03-20            0              0  xbb.1.5    0.000000   
    1677  2023-03-21            1              1  xbb.1.5    1.000000   

          prevalence_rolling  
    1454            0.350000  
    1455            0.179487  
    1456            0.109375  
    1457            0.065421  
    1458            0.058577  
    ...                  ...  
    1673            1.000000  
    1674            1.000000  
    1675            1.000000  
    1676            1.000000  
    1677            1.000000  

[224 rows x 6 columns]
