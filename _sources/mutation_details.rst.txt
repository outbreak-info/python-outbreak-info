mutation_details
----------------------------

.. autofunction:: outbreak_data.mutation_details


Get details on all mutations with "E484" in the name::

      >>> df = outbreak_data.mutation_details('*e484*')
      >>> df

                     type gene ref_codon    pos alt_codon  is_synonymous ref_aa  \
    mutation                                                                       
    S:E484L   substitution    S       GAA  23012       CTT          False      E   
    S:E484A   substitution    S       GAA  23013       GCC          False      E   
    S:E484R   substitution    S       GAA  23012       AGG          False      E   
    S:E484V   substitution    S       GAA  23012       GTG          False      E   
    S:E484T   substitution    S       GAA  23012       ACA          False      E   
    S:E484D   substitution    S       GAA  23012       GAC          False      E   
    S:E484H   substitution    S       GAA  23013       CAT          False      E   
    S:E484K   substitution    S       GAA  23013       AAG          False      E   
    S:E484Q   substitution    S       GAA  23011       CAA          False      E   
    S:E484I   substitution    S       GAA  23011       ATA          False      E   

              codon_num alt_aa  
    mutation                    
    S:E484L         484      L  
    S:E484A         484      A  
    S:E484R         484      R  
    S:E484V         484      V  
    S:E484T         484      T  
    S:E484D         484      D  
    S:E484H         484      H  
    S:E484K         484      K  
    S:E484Q         484      Q  
    S:E484I         484      I 
