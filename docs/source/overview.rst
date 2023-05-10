========================
Software Structure
========================

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
