mutation_prevalences
---------------------

.. autofunction:: outbreak_data.mutation_prevalences

**Example Usage**

Get prevalence data on mutations orf1b:r1315c and s:l24s under lineage BA.2.86 in the US::


    >>> df = outbreak_data.mutation_prevalences('orf1b:r1315c, s:l24s', 'USA' ,'BA.2.86')
    >>> df

	         pangolin_lineage  lineage_count  mutation_count  proportion  \
    query                                                                      
    s:l24s                ba.2.86             84              77    0.916667   
    orf1b:r1315c          ba.2.86             84              84    1.000000   

                  proportion_ci_lower  proportion_ci_upper  
    query                                                   
    s:l24s                   0.843358             0.961949  
    orf1b:r1315c             0.970625             0.999994  
