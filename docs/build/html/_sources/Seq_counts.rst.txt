sequence_counts(location, cumulative, sub_admin)
-------------------------------------------------

.. autofunction:: outbreak_data.sequence_counts

Example usage:

1. Get number of daily sequence counts in the US::
   
    df = od.sequence_counts('USA')
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

2. Get total number of sequence counts

    df = od.sequence_counts('USA', cumulative=True)
    print(df)

.. code-block::
   :caption: Output

                  Values
    total_count  4617418


