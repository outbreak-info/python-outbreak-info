cases_by_location(location)
-----------------------------------
 
.. autofunction:: outbreak_data.cases_by_location

Example usage::

    #Get the number of SARS-CoV-2 cases in Colorado.
    df = outbreak_data.cases_by_location('USA_US-CO')
    print(df)

.. code-block::
   :caption: Output:

                                 _id    _score    admin1   confirmed_numIncrease  \
    0     USA_Colorado_None2021-03-14  8.438688  Colorado                    505   
    1     USA_Colorado_None2021-03-18  8.438688  Colorado                   1060   
    2     USA_Colorado_None2021-03-20  8.438688  Colorado                    852   
    3     USA_Colorado_None2021-03-26  8.438688  Colorado                   1184   
    4     USA_Colorado_None2021-04-07  8.438688  Colorado                   1897   
    ...                           ...       ...       ...                    ...   
    1116  USA_Colorado_None2022-06-22  8.397695  Colorado                   2226   
    1117  USA_Colorado_None2022-06-29  8.397695  Colorado                   2402   
    1118  USA_Colorado_None2022-07-09  8.397695  Colorado                   1348   
    1119  USA_Colorado_None2022-07-14  8.397695  Colorado                   1924   
    1120  USA_Colorado_None2022-07-16  8.397695  Colorado                   1231   

                date  
    0     2021-03-14  
    1     2021-03-18  
    2     2021-03-20  
    3     2021-03-26  
    4     2021-04-07  
    ...          ...  
    1116  2022-06-22  
    1117  2022-06-29  
    1118  2022-07-09  
    1119  2022-07-14  
    1120  2022-07-16  

[1121 rows x 5 columns]
