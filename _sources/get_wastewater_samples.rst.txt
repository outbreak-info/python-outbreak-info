get_wastewater_samples
------------------------

.. autofunction:: outbreak_data.get_wastewater_samples

**Example Usage**

Find wastewater sample data at a specified collection site and minimum viral_load between 2023-09-01 to the last date for wastewater data collection in Ohio::

    # Use get_wastewater_latest() to get the last collection date for wastewater data

    >>> last_ww_date = latest_ww_date = outbreak_data.get_wastewater_latest(region="Ohio", server='dev.outbreak.info')

    >>> outbreak_data.get_wastewater_samples(collection_site_id="USA_OH_5f9e5487", viral_load_at_least=25000, date_range=["2023-09-01", last_ww_date], server='dev.outbreak.info')

                    collection_site_id  \
    collection_date                      
    2023-09-06         USA_OH_5f9e5487   
    2023-09-25         USA_OH_5f9e5487   
    2023-09-18         USA_OH_5f9e5487   

                                                    coverage_intervals  \
    collection_date                                                      
    2023-09-06       [[34, 2243], [2491, 2877], [3083, 3485], [4625...   
    2023-09-25       [[970, 1333], [1566, 1921], [2184, 2540], [310...   
    2023-09-18       [[670, 1013], [1566, 1921], [2512, 3765], [402...   

                     demix_success geo_loc_country geo_loc_region sra_accession  \
    collection_date                                                               
    2023-09-06                True             USA           Ohio   SRR26133858   
    2023-09-25                True             USA           Ohio   SRR26549478   
    2023-09-18                True             USA           Ohio   SRR26549479   

                     variants_success  viral_load  ww_population  \
    collection_date                                                
    2023-09-06                   True     98147.5         226729   
    2023-09-25                   True     51116.0         226729   
    2023-09-18                   True     40253.0         226729   

                     normed_viral_load  
    collection_date                     
    2023-09-06                3.189438  
    2023-09-25                1.661085  
    2023-09-18                1.308077  

                   
