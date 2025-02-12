most_recent_cl_data
---------------------

.. autofunction:: outbreak_data.most_recent_cl_data

**Example Usage**

View the last date of sample matching  for BA.2.86 in New York::
  
    >>> date = outbreak_data.most_recent_cl_data('BA.2.86', location = 'USA_US-NY' )
    >>> date

    Timestamp('2024-01-16 00:00:00')
