daily_lag
---------------

.. autofunction:: outbreak_data.daily_lag

**Example Usage**

Get the daily lag for SARS-Cov-2 data in Hawaii::

    >>> df = outbreak_data.daily_lag('USA_US-HI')
    >>> df
                                   total_count
    date_collected date_submitted             
    2020-03-05     2020-04-16                1
    2020-03-07     2020-04-16                1
    2020-03-11     2020-12-31                1
    2020-03-12     2020-06-16                2
                   2020-12-31                1
    ...                                    ...
    2024-04-24     2024-05-08                3
                   2024-05-16                2
    2024-04-25     2024-05-16                2
    2024-04-27     2024-05-16                1
    2024-04-30     2024-05-16                1

    [5798 rows x 1 columns]
