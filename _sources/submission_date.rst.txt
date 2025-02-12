submission_date(pango_lin, mutations=None, location)
----------------------------------------------------

.. autofunction:: outbreak_data.submission_date

Example usage::

    df = outbreak_data.submission_date('xbb.1', location='USA')
    print(df)

.. code-block::
   :caption: Output

                    Values
    date        2023-06-16
    date_count           5
