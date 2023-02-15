.. Py_Outbreak_API documentation master file, created by
   sphinx-quickstart on Sat Oct  8 22:16:44 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Python Outbreak.info API's documentation!
========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Here you can find information on the functions you will use to collect and analyze SARS-COV-2  data from the Outbreak.info API. 
Our package pulls data from the `Outbreak.info API  <https://api.outbreak.info/>`_ and is reflected on our `Outbreak.info web interface <https://outbreak.info/>`_

Getting Started
----------------

To start using the Python Outbreak package, please run 

```
python authenticate_user.py
```

and login using your GISAID credentials in order to generate an API key.

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   Outbreak_data Functions
   Cases_by_location
   Lineage_mutations
   Prevalence_by_location
   Global_Prev
   Seq_counts
   Mut_By_Lin
   auth_setup
   daily_prev_by_location
   collection_date
   mutation_details
   daily_lag
