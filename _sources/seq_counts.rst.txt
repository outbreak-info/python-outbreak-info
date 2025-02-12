sequence_counts
-----------------------

.. autofunction:: outbreak_data.sequence_counts

**Example Usage**

Get number of daily sequence counts in New York, Colorado, Florida and Texas::

    >>> df = outbreak_data.sequence_counts('USA', sub_admin = True)
    >>> states = df.loc[['USA_US-NY', 'USA_US-FL', 'USA_US-CO', 'USA_US-TX']]
    >>> states

                 total_count
    location_id             
    USA_US-NY         346598
    USA_US-FL         211068
    USA_US-CO         243188
    USA_US-TX         302701
   

