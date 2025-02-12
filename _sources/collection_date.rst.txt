collection_date(pango_lin, mutations=None, location=None)
----------------------------------------------------------

.. autofunction:: outbreak_data.collection_date

Example usage::

    df = od.collection_date('b.1.1.7', location='IND')
    print(df)

.. code-block::
   :caption: Output
                    
                    Values
    date        2021-11-26
    date_count           2
