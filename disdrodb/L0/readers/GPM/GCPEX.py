#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------.
# Copyright (c) 2021-2022 DISDRODB developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------.
from disdrodb.L0 import run_L0
from disdrodb.L0.L0_processing import reader_generic_docstring, is_documented_by


@is_documented_by(reader_generic_docstring)
def reader(
    raw_dir,
    processed_dir,
    l0a_processing=True,
    l0b_processing=True,
    keep_l0a=False,
    force=False,
    verbose=False,
    debugging_mode=False,
    lazy=True,
    single_netcdf=True,
):

    ##------------------------------------------------------------------------.
    #### - Define column names
    column_names = ["time", "TO_BE_SPLITTED"]

    ##------------------------------------------------------------------------.
    #### - Define reader options
    reader_kwargs = {}
    # Skip first row as columns names
    reader_kwargs["header"] = None
    # Skip file with encoding errors
    reader_kwargs["encoding_errors"] = "ignore"
    # - Need for zipped raw file (GPM files)
    reader_kwargs["zipped"] = True
    # Searched file into tar files
    reader_kwargs["file_name_to_read_zipped"] = "raw.txt"
    # - Define delimiter
    reader_kwargs["delimiter"] = ";"
    # - Avoid first column to become df index !!!
    reader_kwargs["index_col"] = False
    # - Define behaviour when encountering bad lines
    reader_kwargs["on_bad_lines"] = "skip"
    # - Define reader engine
    #   - C engine is faster
    #   - Python engine is more feature-complete
    reader_kwargs["engine"] = "python"
    # - Define on-the-fly decompression of on-disk data
    #   - Available: gzip, bz2, zip
    reader_kwargs["compression"] = "infer"
    # - Strings to recognize as NA/NaN and replace with standard NA flags
    #   - Already included: ‘#N/A’, ‘#N/A N/A’, ‘#NA’, ‘-1.#IND’, ‘-1.#QNAN’,
    #                       ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘<NA>’, ‘N/A’,
    #                       ‘NA’, ‘NULL’, ‘NaN’, ‘n/a’, ‘nan’, ‘null’
    reader_kwargs["na_values"] = ["na", "", "error", "NA", "-.-"]
    # - Define max size of dask dataframe chunks (if lazy=True)
    #   - If None: use a single block for each file
    #   - Otherwise: "<max_file_size>MB" by which to cut up larger files
    reader_kwargs["blocksize"] = None  # "50MB"

    ##------------------------------------------------------------------------.
    #### - Define dataframe sanitizer function for L0 processing
    def df_sanitizer_fun(df, lazy=False):
        # - Import dask or pandas
        if lazy:
            import dask.dataframe as dd
        else:
            import pandas as dd

        # - Define 'time' datetime
        df_time = dd.to_datetime(df["time"], format="%Y%m%d%H%M%S")

        # - Split the 'TO_BE_SPLITTED' column
        df = df["TO_BE_SPLITTED"].str.split(",", n=9, expand=True)

        # - Assign column names
        column_names = [
            "sensor_id",
            "sensor_status",
            "sensor_temperature",
            "number_particles",
            "rainfall_rate_32bit",
            "reflectivity_32bit",
            "mor_visibility",
            "weather_code_synop_4680",
            "weather_code_synop_4677",
            "raw_drop_number",
        ]
        df.columns = column_names

        # - Add the time column
        df["time"] = df_time

        # - Drop columns not agreeing with DISDRODB L0 standards
        df = df.drop(columns=["sensor_id"])
        return df

    ##------------------------------------------------------------------------.
    #### - Define glob pattern to search data files in <raw_dir>/data/<station_id>
    files_glob_pattern = "*.tar"

    ####----------------------------------------------------------------------.
    #### - Create L0 products
    run_L0(
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        l0a_processing=l0a_processing,
        l0b_processing=l0b_processing,
        keep_l0a=keep_l0a,
        force=force,
        verbose=verbose,
        debugging_mode=debugging_mode,
        lazy=lazy,
        single_netcdf=single_netcdf,
        # Custom arguments of the reader
        files_glob_pattern=files_glob_pattern,
        column_names=column_names,
        reader_kwargs=reader_kwargs,
        df_sanitizer_fun=df_sanitizer_fun,
    )
