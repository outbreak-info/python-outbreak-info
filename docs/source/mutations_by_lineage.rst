mutations_by_lineage(mutation, location, pango_lin)
---------------------------------------------------

.. autofunction:: outbreak_data.mutations_by_lineage


Example usage::

    #Get info on mutation 'orf1b:p314l'
    df = od.mutations_by_lineage('orf1b:p314l')
    print(df)

.. code-block::
   :caption: Output

            pangolin_lineage  lineage_count  mutation_count  proportion  \
    0                   ba.2        1227503         1222717    0.996101   
    1                b.1.1.7        1154337         1147331    0.993931   
    2                 ba.1.1        1044480         1039813    0.995532   
    3                   ay.4         858839          854935    0.995454   
    4                   ba.1         438947          437207    0.996036   
    ...                  ...            ...             ...         ...   
    2851                fn.1              1               1    1.000000   
    2852  miscba1ba2post5386              1               1    1.000000   
    2853            xbb.1.23              1               1    1.000000   
    2854            xbb.1.37              1               1    1.000000   
    2855                 xbv              1               1    1.000000   

          proportion_ci_lower  proportion_ci_upper  
    0                0.995990             0.996210  
    1                0.993788             0.994071  
    2                0.995402             0.995658  
    3                0.995310             0.995595  
    4                0.995847             0.996219  
    ...                   ...                  ...  
    2851             0.146746             0.999614  
    2852             0.146746             0.999614  
    2853             0.146746             0.999614  
    2854             0.146746             0.999614  
    2855             0.146746             0.999614  

[2856 rows x 6 columns]


