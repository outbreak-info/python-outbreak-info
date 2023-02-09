lineage_mutations(pango_lin, mutation, freq)
--------------------------------------------

.. autofunction:: outbreak_data.lineage_mutations
 
.. code-block::
   :caption: Example usage:
   
        foo = lineage_mutations('b.1.1.7')

.. code-block::
   :caption: Mutiple queries for lineages and mutations can be separated by ","

        Ex:  foo = lineage_mutations('b.1.1.7, b.2, ay.2')

.. code-block::
   :caption: Use 'OR' in a string to return overlapping mutations in multiple lineages.

        Ex:  foo = lineage_mutations('ba.2 OR b.1.1.7')


