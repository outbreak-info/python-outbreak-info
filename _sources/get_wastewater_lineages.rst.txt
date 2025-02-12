get_wastewater_lineages
------------------------

.. autofunction:: outbreak_data.get_wastewater_lineages


Note that this function is used in conjunction with get_wastewater_mutations.

**Example Usage**

Find lineages of samples associated with A --> G base mutations at genome position 1003:: 
    
    # Collect wastewater mutation data
    >>> samples = outbreak_data.get_wastewater_samples_by_mutation(site=1003, alt_base='G', server='dev.outbreak.info')

    >>> outbreak_data.get_wastewater_lineages(samples, server='dev.outbreak.info')

                                alt_base  depth  prevalence_x ref_base  site  \
    mutation            lineage                                                 
    1003 AND alt_base:G CK.1.1.1        G     51      0.038088        A  1003   
                        CL.1.3          G     51      0.038088        A  1003   
                        DV.1.1          G     51      0.038088        A  1003   
                        HW.1            G     51      0.038088        A  1003   
                        XBJ.4           G     51      0.038088        A  1003   
    ...                               ...    ...           ...      ...   ...   
                        JR.1.1.1        G     23      0.273810        A  1003   
                        JY.1.1          G     23      0.273810        A  1003   
                        KE.3            G     23      0.273810        A  1003   
                        KT.1.1          G     23      0.273810        A  1003   
                        XBB.1.24        G     23      0.273810        A  1003   

                                 sra_accession        query   coverage  \
    mutation            lineage                                          
    1003 AND alt_base:G CK.1.1.1   SRR21864715  SRR21864715  97.555429   
                        CL.1.3     SRR21864715  SRR21864715  97.555429   
                        DV.1.1     SRR21864715  SRR21864715  97.555429   
                        HW.1       SRR21864715  SRR21864715  97.555429   
                        XBJ.4      SRR21864715  SRR21864715  97.555429   
    ...                                    ...          ...        ...   
                        JR.1.1.1   SRR25022780  SRR25022780   9.848510   
                        JY.1.1     SRR25022780  SRR25022780   9.848510   
                        KE.3       SRR25022780  SRR25022780   9.848510   
                        KT.1.1     SRR25022780  SRR25022780   9.848510   
                        XBB.1.24   SRR25022780  SRR25022780   9.848510   

                                                                             crumbs  \
    mutation            lineage                                                       
    1003 AND alt_base:G CK.1.1.1  ;B;B.1;B.1.1;B.1.1.529;B.1.1.529.5;B.1.1.529.5...   
                        CL.1.3    ;B;B.1;B.1.1;B.1.1.529;B.1.1.529.5;B.1.1.529.5...   
                        DV.1.1    ;B;B.1;B.1.1;B.1.1.529;B.1.1.529.2;B.1.1.529.2...   
                        HW.1      ;XBC;XBC.1;XBC.1.6;XBC.1.6.3;XBC.1.6.3.1;HW;HW.1;   
                        XBJ.4                                           ;XBJ;XBJ.4;   
    ...                                                                         ...   
                        JR.1.1.1  ;XBB;XBB.1;XBB.1.9;XBB.1.9.2;XBB.1.9.2.5;XBB.1...   
                        JY.1.1    ;XBB;XBB.2;XBB.2.3;XBB.2.3.19;XBB.2.3.19.1;XBB...   
                        KE.3      ;XBB;XBB.1;XBB.1.19;XBB.1.19.1;XBB.1.19.1.5;XB...   
                        KT.1.1    ;XBB;XBB.2;XBB.2.3;XBB.2.3.10;XBB.2.3.10.1;XBB...   
                        XBB.1.24                               ;XBB;XBB.1;XBB.1.24;   

                                  prevalence_y  spike_coverage  
    mutation            lineage                                 
    1003 AND alt_base:G CK.1.1.1      0.000530       98.874935  
                        CL.1.3        0.000550       98.874935  
                        DV.1.1        0.000106       98.874935  
                        HW.1          0.000220       98.874935  
                        XBJ.4         0.000288       98.874935  
    ...                                    ...             ...  
                        JR.1.1.1      0.131121        3.218210  
                        JY.1.1        0.100538        3.218210  
                        KE.3          0.008403        3.218210  
                        KT.1.1        0.238095        3.218210  
                        XBB.1.24      0.018568        3.218210  

    [6085 rows x 11 columns]
