=========================
Data
=========================


Access to the raw disdrometer measurements and metadata is available through a
separate GitHub repository : `disdrodb-data <https://github.com/ltelab/disdrodb-data>`__.

The `disdrodb-data` GitHub repository includes:

* The stations measurements in the form of a JSON file with URLs links to the downloadable data (not included in the repository due to GitHub's file size limitation).
* The stations metadata in YAML file format.
* The stations issue in YAML file format.
* Some python code to download the datasets using the URLs provided in the JSON files.
* Some python code to curate the metadata archive.


You can clone the disdrodb-data repository with 

.. code-block:: bash

   git clone https://github.com/ltelab/disdrodb-data.git
   
   
However, if you plan to add new data or metadata to the archive, first fork the 
repository on your GitHub account and then clone the forked repository.

Download DISDRODB Raw Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

To get the measurements locally, just run the following python command :


.. code-block:: python

   cd <app folder path>
   python download_data.py


This code parses all json files and download the corresponding data.

If you want to download only one specific folder (data_source, campaign_name, station_name) :


.. code-block:: python

   cd <app folder path>
   python download_data.py -data_source <your-data-source> -campaign_name <your-campaign-name> -station_name <you-station-name>


By default, if a file is already in the local folder, it will not be overwritten. If you want to change this behavior and overwrite existing files, add the `-overwrite` parameter as follow :


.. code-block:: python

   cd <app folder path>
   python download_data.py -overwrite True



Upload DISDRODB Raw Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

Do you want to contribute to the project with your own data ? Great ! Just follow these steps :

#. Create a new branch

   .. code-block:: python
      
      git checkout -b "reader-<data_source>-<campaign_name>"

#. Add the your data source, campaign names, station name to the current folder structure.

#. Load your data to an external repository (eg. Zenodo). Github limits the file size to 50 MB, therefore no data can be loaded into the github repository.

#. For each campaign, create a url.json file and add the following information :

   .. code-block:: json
      
      {"<the-file-name>":"<the_url>"},

#. Add your metadata YAML file for each station station_name.yml, in a metadata directory in the campaign directory. We recommend you to copy-paste an existing metadata YAML file to get the correct structure.

#. (Optional) Add your issues YAML files, for each station station_name.yml, in an issue directory located in the campaign directory. We recommend you to copy-paste an existing metadata YAML file to get the correct structure.

#. Test that the integration of your new dataset functions, by deleting your data locally - and re-fetching it through the process detailed in (A).

#. Commit your changes and push your branch to GitHub

#. `Create a pull request <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__, and wait for a maintainer to accepts it !

If you struggle with this process, don't hesitate to raise an `issue <https://github.com/ltelab/disdrodb-data/issues/new/choose>`__ so we can help!
 
 
 Upload DISDRODB Raw Data to zeneodo
 -------------------------------------

 to do from https://github.com/ltelab/disdrodb-data/tree/main/app/upload_to_zenodo