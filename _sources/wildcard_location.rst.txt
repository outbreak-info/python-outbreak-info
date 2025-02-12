wildcard_location
------------------------

.. autofunction:: outbreak_data.wildcard_location

**Example Usage**

List locations containing 'awai' in the name::

    >>> df = outbreak_data.wildcard_location('*awai*')
    >>> df

                           country country_id   division division_id  \
    id                                                                 
    USA_US-HI        United States        USA     Hawaii          HI   
    USA_US-HI_15001  United States        USA     Hawaii          HI   
    IND_IN-RJ_SM             India        IND  Rajasthan          RJ   

                                                label  admin_level  total_count  \
    id                                                                            
    USA_US-HI                   Hawaii, United States            1        28332   
    USA_US-HI_15001     Hawaii, Hawaii, United States            2         3325   
    IND_IN-RJ_SM     Sawai Madhopur, Rajasthan, India            2          138   

                           location location_id  
    id                                           
    USA_US-HI                   NaN         NaN  
    USA_US-HI_15001          Hawaii       15001  
    IND_IN-RJ_SM     Sawai Madhopur          SM  

