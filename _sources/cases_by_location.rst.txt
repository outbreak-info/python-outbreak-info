cases_by_location
---------------------
 
.. autofunction:: outbreak_data.cases_by_location

**Example Usage**

Get the number of SARS-CoV-2 cases in Colorado::

    >>> df = outbreak_data.cases_by_location('USA_US-CO', 2)
    >>> df

                                  confirmed_numIncrease  confirmed_rolling
    location          date                                                
    USA_Colorado_None 2020-02-12                      0           0.000000
                      2020-02-13                      0           0.000000
                      2020-02-14                      0           0.000000
                      2020-02-15                      0           0.000000
                      2020-02-16                      0           0.000000
    ...                                             ...                ...
                      2023-03-04                      0         436.000000
                      2023-03-05                      0         436.000000
                      2023-03-06                    553         440.428558
                      2023-03-07                      0         440.428558
                      2023-03-08                    827         438.428558

    [1121 rows x 2 columns]
