.. Py_Outbreak_API documentation master file, created by
   sphinx-quickstart on Sat Oct  8 22:16:44 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Python Outbreak.info package docs!
========================================================
Here you can find information on the functions you will use to collect and analyze SARS-COV-2  data from the Outbreak.info API. 
Our package pulls data from the `Outbreak.info API  <https://api.outbreak.info/>`_ and is reflected on our `Outbreak.info web interface <https://outbreak.info/>`_

Installation
----------------
We recommend installing the package via pip using:

``pip install python-outbreak-info``

Alternatively, the package can be directly installed from source via pip:

``pip install git+https://github.com/outbreak-info/python-outbreak-info.git``

Getting Started
----------------
The Python Outbreak.info package contains key functions for accessing genomic and epidemiological data for SARS-CoV-2. Access to genomic data requires logging in using GISAID credentials to generate an API key, using the ``authenticate_new_user()`` function. To perform authentication, you'll need to first run

.. code-block:: python

   from outbreak_data import authenticate_user
   authenticate_user.authenticate_new_user()

and then you should be able access all of the functionality of the package. Most of the rest of the tools are available within the ``outbreak_data`` component of the package. For example: 

.. code-block:: python

   from outbreak_data import outbreak_data
   lin_list = ['B.1.1.7','B.1.351','B.1.617.2']
   # request lineages occurring with minimum frequency of 0.05 (5%)
   df = outbreak_data.lineage_mutations(lin_list,freq=0.05)
   # filter mutations and sort by codon number
   df = df[df['gene']=='S'].sort_values(by='codon_num')

For location-specific analyses, users will need to supply the appropriate location code corresponding to their location of interest. To do this, we provide an ID lookup tool kit via the ``outbreak_tools`` part of the package. An example lookup should look like: 

.. code-block:: python

   from outbreak_tools import outbreak_tools
   location_list = outbreak_tools.id_lookup(['Illinois','South Africa','Chile'])
   # which returns ['USA_US-IL', 'ZAF', 'CHL']


.. note::

   This project is under active development.

Core Outbreak Data Tools
--------------------------
.. toctree::
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
   Outbreak_data Functions
   id_lookup

Example analyses:
--------------------------
Coming soon 
