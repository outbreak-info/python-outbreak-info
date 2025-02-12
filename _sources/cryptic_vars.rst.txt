Tracing Mutations Back to Lineage
--------------------------------- 
 
The Python Outbreak API can be queried in order to determine which lineages a mutation has been found in. After collecting a sample and determining what sequences are present, we may have a list of several SARS-CoV-2 mutations that we can immediately say are characteristic of a specific variant. However in some cases, we also may have a mutation that is relatively uncommon in most other samples. 
For example, we can look at small data sample consisting of 10 mutations: (S:A67V, S:DEL69/70, S:E484A, S:N501Y, S:T572N, S:D614G, S:G142D  N:S2Y, S:Q52R, E:L21F, S:G593D). We’ll want a way to find more details about any mutation collected, such as whether the mutation has been collected before, when, and where that mutation came from.

To start, the ``mutation_prevalences()`` function allows us to look at the clinical prevalence of a mutation and see which lineage it most likely belongs to. Let's try it for E:L21F::

    # Perform authentication if you haven't already
    from outbreak_data import authenticate_user
    authenticate_user.authenticate_new_user()

    # Import outbreak_data package
    from outbreak_data import outbreak_data as od

    lin1 = od.mutation_prevalences(mutation='E:L21F')
    print(lin1)

.. code-block::
   :caption: Output

             pangolin_lineage  lineage_count  mutation_count  proportion  \    
        0               ba.2        1228296             560    0.000456   
        1            b.1.1.7        1155169             844    0.000731   
        2             ba.1.1        1046121             268    0.000256   
        3               ay.4         861521             526    0.000611   
        4               ba.1         439838              49    0.000111   
        ...               ...            ...             ...         ...   
        400          ba.2.77             63              48    0.761905   
        401        ba.5.2.54             55               2    0.036364   
        402          b.1.616             39               3    0.076923   
        403        b.1.1.386             20               1    0.050000   
        404        b.1.1.400             20              20    1.000000   

             proportion_ci_lower  proportion_ci_upper  
        0               0.000419             0.000495  
        1               0.000683             0.000781  
        2               0.000227             0.000288  
        3               0.000560             0.000664  
        4               0.000083             0.000146  
        ...                   ...                  ...  
        400             0.646596             0.853783  
        401             0.007632             0.111568  
        402             0.022142             0.191265  
        403             0.005449             0.210819  
        404             0.883361             0.999976  

[405 rows x 6 columns]

This mutation has clearly been seen before in some previous lineages. We might be able recognize that most of the mutations in our list have been detected in older variants, as well as Omicron. However, S:G593D is relatively uncommon in most other samples. We can easily find out where and when it was last detected::

   >>>  lin2 = od.mutation_prevalences(mutation='S:G593D')
   >>>  print(lin2)

        pangolin_lineage  lineage_count  mutation_count  proportion  \
    0            xbb.1          28205               1    0.000035   

       proportion_ci_lower  proportion_ci_upper  
    0             0.000004             0.000166  

   
   >>>  last_seen = od.most_recent_cl_data('xbb.1', 'S:G593D')
   >>>  print(last_seen)

   Timestamp(2022-12-22 00:00:00)

According to our data, S:G593D has only been detected once in a single sequence belonging to the xbb.1 lineage. The last time it was collected was back on December 12, 2022. 

Additionally ``mutation_prevalences`` allows us to find out if there is a lineage where several mutations overlap. Selecting 7 of the mutations from our original list yields one lineage with all of these mutation characteristics::

    >>> lin3 = od.mutation_prevalences(mutation='S:A67V, S:DEL69/70, S:E484A, S:N501Y, S:T572N, S:D614G, S:G142D')
    >>> print(lin3)

         pangolin_lineage  lineage_count  mutation_count  proportion  \
       0          ba.1.19           4587               1    0.000218   

       proportion_ci_lower  proportion_ci_upper  
    0             0.000024             0.001019 


Here we see that the only lineage that contains all 7 mutations is ba.1.19. 


