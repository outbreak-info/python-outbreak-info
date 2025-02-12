known_mutations
-----------------

.. autofunction:: outbreak_data.known_mutations

**Example Usage**

Get info on all mutations under "BA.2.86"::

    >>> df = outbreak_data.known_mutations('BA.2.86')
    >>> df

       mutation_count  lineage_count  lineage   gene      ref_aa  \
    mutation                                                                  
    e:t9i                    995            995  BA.2.86      E           T   
    orf1b:r1315c             995            995  BA.2.86  ORF1b           R   
    orf1b:p314l              994            995  BA.2.86  ORF1b           P   
    orf3a:t223i              994            995  BA.2.86  ORF3a           T   
    n:r203k                  992            995  BA.2.86      N           R   
    ...                      ...            ...      ...    ...         ...   
    s:r403k                  858            995  BA.2.86      S           R   
    s:del25/27               832            995  BA.2.86      S  S:DEL25/27   
    s:l24s                   832            995  BA.2.86      S           L   
    s:n460k                  808            995  BA.2.86      S           N   
    s:s477n                  799            995  BA.2.86      S           S   

                    alt_aa  codon_num  codon_end          type  prevalence  \
    mutation                                                                 
    e:t9i                I          9        NaN  substitution    1.000000   
    orf1b:r1315c         C       1315        NaN  substitution    1.000000   
    orf1b:p314l          L        314        NaN  substitution    0.998995   
    orf3a:t223i          I        223        NaN  substitution    0.998995   
    n:r203k              K        203        NaN  substitution    0.996985   
    ...                ...        ...        ...           ...         ...   
    s:r403k              K        403        NaN  substitution    0.862312   
    s:del25/27    DEL25/27         25       27.0      deletion    0.836181   
    s:l24s               S         24        NaN  substitution    0.836181   
    s:n460k              K        460        NaN  substitution    0.812060   
    s:s477n              N        477        NaN  substitution    0.803015   

                  change_length_nt  
    mutation                        
    e:t9i                      NaN  
    orf1b:r1315c               NaN  
    orf1b:p314l                NaN  
    orf3a:t223i                NaN  
    n:r203k                    NaN  
    ...                        ...  
    s:r403k                    NaN  
    s:del25/27                 9.0  
    s:l24s                     NaN  
    s:n460k                    NaN  
    s:s477n                    NaN  

    [81 rows x 11 columns]
