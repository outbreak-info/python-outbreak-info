get_wastewater_latest
----------------------

.. autofunction:: outbreak_data.get_wastewater_latest


**Example Usage**
  
Get the most recent date for wastewater data collection in Ohio::

    >>> outbreak_data.get_wastewater_latest(region="Ohio", server='dev.outbreak.info')

    [Out]: '2023-10-01'
