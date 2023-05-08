========================
Software Structure
========================


Overview of the disdrodb project folders structure
============================================================


The current software structure is described below:

| 📁 data/
| 📁 disdrodb/
| ├── 📁 api
|     ├── 📜 checks.py
|     ├── 📜 info.py
|     ├── 📜 io.py
|     ├── 📜 metadata.py
| ├── 📁 data_transfer
|     ├── 📜 download_data.py
|     ├── 📜 upload_data.py
| ├── 📁 l0
|     ├── 📁 configs
|     	├── 📁 `<sensor_name>`
|     		├── 📜 \*.yml
|     ├── 📁 manuals
|       ├── 📜 \*.pdf
|     ├── 📁 readers
|     	├── 📁 `<data_source>`
|           ├── 📜 \<reader_name>.py
|     ├── 📁 scripts
|         ├── 📜 run_disdrodb_l0_station.py
|         ├── 📜 run_disdrodb_l0
|         ├── 📜 run_disdrodb_l0a.py
|         ├── 📜 run_disdrodb_l0a_station.py
|         ├── 📜 run_disdrodb_l0b.py
|         ├── 📜 run_disdrodb_l0b_station.py
|         ├── 📜 run_disdrodb_l0b_concat.py
|         ├── 📜 run_disdrodb_l0b_concat_station.py
|     ├── 📜 check_configs.py
|     ├── 📜 check_metadata.py
|     ├── 📜 check_standards.py
|     ├── 📜 io.py
|     ├── 📜 issue.py
|     ├── 📜 l0_processing.py
|     ├── 📜 l0a_processing.py
|     ├── 📜 l0b_processing.py
|     ├── 📜 l0b_concat.py
|     ├── 📜 l0b_processing.py
|     ├── 📜 l0_reader.py
|     ├── 📜 metadata.py
|     ├── 📜 standards.py
|     ├── 📜 summary.py
|     ├── 📜 template_tools.py
| ├── 📁 l1/
| ├── 📁 l2/
| ├── 📁 tests/
|   ├── 📜 \*.py
| ├── 📁 api/
| ├── 📁 utils/
|   ├── 📜 logger.py
|   ├── 📜 scripts.py
|   ├── 📜 netcdf.py
| 📁 docs/
| 📁 tutorials
| 📜 .gitignore
| 📜 .pre-commit-config.yaml
| 📜 CODE_OF_CONDUCT.md
| 📜 CONTRIBUTING.rst
| 📜 environment.yml
| 📜 LICENSE
| 📜 MANIFEST.in
| 📜 pyproject.toml
| 📜 README.md
| 📜 readthedocs.yml
| 📜 requirements.txt




Description of the disdrodb files and folders
================================================

The disdrodb folder contains the core software to process raw data files to DISDRODB L0 products. Here is a description of the files and folders:

+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Type  | Folder / files name                | Description                                                                                                  |
+=======+====================================+==============================================================================================================+
| 📁    | api                                | Contains some generic functions                                                                              |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | checks.py                          | Basic checks on paths                                                                                        |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | info.py                            | DISDRODB File Information and parser                                                                         |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | io.py                              | Input output fuctions                                                                                        |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | metadata.py                        | Operation on metadata stations files                                                                         |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | data_transfer                      | Contains scripts to upload or download stations's data                                                       |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | download_data.py                   | Functions to download stations' raw data                                                                     |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | upload_data.py                     | Functions to upload to Zenodo stations' raw data                                                             |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | l0                                 | Contains the software to produce the DISDRODB L0 products                                                    |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | check_configs.py                   | Contain functionsChecking the sensorConfigs YAML files                                                       |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | check_metadata.py                  | Contain functionsChecking the metadata YAML files                                                            |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | check_standards.py                 | Contain functionsChecking that DISDRODB standards are met                                                    |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | io.py                              | Core functions to read/write files andCreate/remove directories                                              |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | issue.py                           | Code to manage the issues YAML files and exclude erroneous time steps during L0 processing                   |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0_processing.py                   | Contain the functions to process raw data files to L0A and L0B                                               |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0_reader.py                       | Contain the functions to check and retrieve the DISDRODB readers                                             |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0a_processing.py                  | Contain the functions to process raw data files to L0A format (Parquet)                                      |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0b_concat.py                      | Contain the functions to concatenate multiple L0B files into a single L0B netCDF                             |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0b_processing.py                  | Contain the functions to process raw data files to L0B format (netCDF4)                                      |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | l0b_processing.py                  | Contain the functions to run the DISDRODB L0 processing                                                      |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | metadata.py                        | Code to read/write the metadata YAML files                                                                   |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | standards.py                       | Contain the functions to encode the L0 sensor specifications defined in L0.configs                           |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | summary.py                         | Contain the functions to define a summary for each station                                                   |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | template_tools.py                  | Helpers to Create DISDRODB readers                                                                           |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | configs                            | Contains the specifications of various types of disdrometers                                                 |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | <sensor_name>                      | Name of the sensor (e.g. OTT_Parsivel, OTT_Parsivel2, Thies_LPM, RD_80)                                      |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | *.yml                              | YAML files defining sensorCharacteristics (e.g. diameter and velocity bins)                                  |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | manuals                            | Folder for the  Official disdrometers documentation                                                          |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | *.pdf                              | Official disdrometers documentation                                                                          |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | readers                            | Folder that contains all the readers functions                                                               |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | <data_source>                      | e.g. GPM, ARM, EPFL, ...                                                                                     |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | <reader_name>.py                   | Readers to transform raw data into DISDRODB L0 products                                                      |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | scripts                            | Contains a set of python scripts to beCalled from the terminal to launch the L0 processing                   |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0_station.py         | Script launching the L0 processing for a specific station                                                    |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0                    | Script launching the L0 processing for specific portion of the DISDRODB archive                              |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0a.py                | Script to run the L0A processing of DISDRODB stations                                                        |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0a_station.py        | Script to run the L0A processing of a specific DISDRODB station from the terminal                            |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0b.py                | Script to run the L0B processing of DISDRODB stations                                                        |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0b_station.py        | Script to run the L0B processing of a specific DISDRODB station from the terminal                            |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0b_concat.py         | Script to run the L0BConcatenation of available DISDRODB stations                                            |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | run_disdrodb_l0b_concat_station.py | Script toConcatenate all L0B files of a specific DISDRODB station into a single netCDF                       |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | l1                                 | Code not yet implemented. It willContain software to homogenize and qualityCheck DISDRODB L0 products        |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | l2                                 | Code not yet implemented. It willContain software to produce DISDRODB L2 products (i.e. DSD parameters, ...) |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | tests                              | Folder containing the tests (readers and unit tests)                                                         |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📁    | utils                              | Folder to gather small, reusable functions orClasses                                                         |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | logger.py                          | Logger functions                                                                                             |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | scripts.py                         | Utility functions to run python scripts into the terminal                                                    |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+
| 📜    | netcdf.py                          | Utility function toCheck and merge/concat multiple netCDF4 files                                             |
+-------+------------------------------------+--------------------------------------------------------------------------------------------------------------+



Description of the other folders
================================================

Some other folder are included in the DISDRODB repository. Here is a short description of their content:

* data : sample data to test the DISDRODB L0 l0_processing
* docs : documentation of the DISDRODB L0 processing
* tutorials : Jupyter notebooks to illustrate the DISDRODB L0 processing
