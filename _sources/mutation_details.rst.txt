mutation_details(mutations)
----------------------------

.. autofunction:: outbreak_data.mutation_details

Example usage::
     
      #Get info on mutation 'orf1b:p314l'
      df = outbreak_data.mutation_details('orf1b:p314l')
      print(df)
  
.. code-block::
     :caption: Output
     
                  Key        Values
      0       mutation   ORF1b:P314L
      1      alt_codon           CTT
      2  is_synonymous         False
      3      codon_num           314
      4      ref_codon           CCT
      5           gene         ORF1b
      6            pos         14407
      7         alt_aa             L
      8         ref_aa             P
      9           type  substitution


