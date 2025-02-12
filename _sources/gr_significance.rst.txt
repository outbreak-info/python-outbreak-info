gr_significance
-----------------

.. autofunction:: outbreak_data.gr_significance

**Example Usage**

Find the tope 5 most significant lineages globally::

    >>> df = outbreak_data.gr_significance(location='Global', n=5)
    >>> df

      _id _score growing   leaf     loc                 sig  \
    lin                                                                         
    JN.1.1    Global_JN.1.1   None    true   true  Global   170.5345544056284   
    JN.1.4    Global_JN.1.4   None    true   true  Global  148.67142485884114   
    JN.1.22  Global_JN.1.22   None    true   true  Global  125.34771448608038   
    JN.1+      Global_JN.1+   None    true  false  Global   115.0086253690486   
    JN.1.7    Global_JN.1.7   None    true   true  Global  103.52483890881427   

                            snr  
    lin                          
    JN.1.1   12.915667590790331  
    JN.1.4   12.041819797365195  
    JN.1.22  11.034042953153367  
    JN.1+    10.556798749279736  
    JN.1.7   10.000270940090726  
