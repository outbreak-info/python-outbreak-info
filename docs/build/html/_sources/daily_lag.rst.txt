daily_lag(location=None)
----------------------------

.. autofunction:: outbreak_data.daily_lag

Example usage::

    df = outbreak_data.daily_lag('LUX')
    print(df)

.. code-block::
   :caption: Output

                 Key      Values             Key      Values             Key  \
    0  date_collected  2020-02-29  date_collected  2020-02-29  date_collected   
    1  date_submitted  2020-03-07  date_submitted  2020-04-02  date_submitted   
    2     total_count           1     total_count           1     total_count   

           Values             Key      Values             Key      Values  ...  \
    0  2020-03-05  date_collected  2020-03-06  date_collected  2020-03-07  ...   
    1  2020-04-02  date_submitted  2020-04-02  date_submitted  2020-04-02  ...   
    2           1     total_count           1     total_count           1  ...   

                  Key      Values             Key      Values             Key  \
    0  date_collected  2023-04-28  date_collected  2023-04-29  date_collected   
    1  date_submitted  2023-05-10  date_submitted  2023-05-10  date_submitted   
    2     total_count          20     total_count          11     total_count   

           Values             Key      Values             Key      Values  
    0  2023-04-30  date_collected  2023-05-01  date_collected  2023-05-02  
    1  2023-05-10  date_submitted  2023-05-10  date_submitted  2023-05-10  
    2           1     total_count           5     total_count           2  
