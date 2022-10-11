#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 09:48:21 2022

@author: kimbo
"""
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

    ####----------------------------------------------------------------------.
    ###########################
    #### CUSTOMIZABLE CODE ####
    ###########################
    #### - Define raw data headers
    # Notes
    # - In all files, the datalogger voltage hasn't the delimeter,
    #   so need to be split to obtain datalogger_voltage and rainfall_rate_32bit

    # These are the variables included in the datasets:

    # var			full name										units

    # Time		time of the record								Y-m-d hh:mm:ss
    # Event		event ID 										(factor)
    # ID			disdromter ID 									(factor: T1, T2, P1, P2)
    # Serial		disdrometer serial number						(factor)
    # Type		disdrometer type 								(factor: Thi, Par)
    # Mast		mast ID											(factor: 1, 2)
    # NP_meas		number of particles detected					(-)
    # R_meas		rainfall intensity, as outputted by the device	mm h−1
    # Z_meas		radar reflectivity, as outputted by the device	dB mm6 m−3
    # E_meas		erosivity, as outputted by the device			J m−2 mm−1
    # Pcum_meas	cumulative rainfall amount						mm
    # Ecum_meas	cumulative kinetic energy						J m−2 mm−1
    # NP			number of particles detected					(-)
    # ND			particle density								m−3 mm−1
    # R			rainfall intensity								mm h−1
    # P			rainfall amount									mm
    # Z			radar reflectivity								dB mm6 m−3
    # M			water content									gm−3
    # E			kinetic energy									J m−2 mm−1
    # Pcum		cumulative rainfall amount						mm
    # Ecum		cumulative kinetic energy						J m−2 mm−1
    # D10			drop diameter’s 10th percentile					mm
    # D25			drop diameter’s 25th percentile					mm
    # D50			drop diameter’s 50th percentile					mm
    # D75			drop diameter’s 75th percentile					mm
    # D90			drop diameter’s 90th percentile					mm
    # Dm			mean drop diameter								mm
    # V10			drop velocity’s 10th percentile					m s−1
    # V25			drop velocity’s 25th percentile					m s−1
    # V50			drop velocity’s 50th percentile					m s−1
    # V75			drop velocity’s 75th percentile					m s−1
    # V90			drop velocity’s 90th percentile					m s−1
    # Vm			mean drop velocity								m s−1

    column_names = [
        "time",
        "id",
        "disdromter_ID",  # to_drop
        "disdrometer_serial",  # to_drop
        "disdrometer_type",  # to_drop
        "mast_ID",  # to_drop
        "number_particles_meas",  # to_drop
        "rainfall_rate_32bit_meas",  # to_drop
        "reflectivity_32bit_meas",  # to_drop
        "mor_visibility_meas",  # to_drop
        "rainfall_accumulated_32bit_meas",  # to_drop
        "rain_kinetic_energy_meas",
        "number_particles",
        "rainfall_rate_32bit",
        "reflectivity_32bit",
        "temp",  # I think is mor_visibility, but not sure about this, give error because values are like: 0.00386755693894061
        "rainfall_accumulated_32bit",
        "rain_kinetic_energy",
        "D10",  # I don't know what to do with this
        "D25",  # I don't know what to do with this
        "D50",  # I don't know what to do with this
        "D75",  # I don't know what to do with this
        "D90",  # I don't know what to do with this
        "Dm",  # I don't know what to do with this
        "V10",  # I don't know what to do with this
        "V25",  # I don't know what to do with this
        "V50",  # I don't know what to do with this
        "V75",  # I don't know what to do with this
        "V90",  # I don't know what to do with this
        "Vm",  # I don't know what to do with this
    ]

    ##------------------------------------------------------------------------.
    #### - Define reader options
    reader_kwargs = {}

    # - Define delimiter
    reader_kwargs["delimiter"] = ","

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

    # Cast all to string
    reader_kwargs["dtype"] = str

    # Skip first row as columns names
    reader_kwargs["header"] = None

    ##------------------------------------------------------------------------.
    #### - Define facultative dataframe sanitizer function for L0 processing
    # - Enable to deal with bad raw data files
    # - Enable to standardize raw data files to L0 standards  (i.e. time to datetime)
    df_sanitizer_fun = None

    def df_sanitizer_fun(df, lazy=False):
        # Import dask or pandas
        if lazy:
            import dask.dataframe as dd
        else:
            import pandas as dd

        # # Drop useless columns
        df = df.drop(
            columns=[
                "id",
                "disdromter_ID",  # to_drop
                "disdrometer_serial",  # to_drop
                "disdrometer_type",  # to_drop
                "mast_ID",  # to_drop
                "number_particles_meas",  # to_drop
                "rainfall_rate_32bit_meas",  # to_drop
                "reflectivity_32bit_meas",  # to_drop
                "temp",  # I think is mor_visibility, but not sure about this, give error because values are like: 0.00386755693894061
                "mor_visibility_meas",  # to_drop
                "rainfall_accumulated_32bit_meas",  # to_drop
                "rain_kinetic_energy_meas",
                "D10",  # I don't know what to do with this
                "D25",  # I don't know what to do with this
                "D50",  # I don't know what to do with this
                "D75",  # I don't know what to do with this
                "D90",  # I don't know what to do with this
                "Dm",  # I don't know what to do with this
                "V10",  # I don't know what to do with this
                "V25",  # I don't know what to do with this
                "V50",  # I don't know what to do with this
                "V75",  # I don't know what to do with this
                "V90",  # I don't know what to do with this
                "Vm",  # I don't know what to do with this
            ]
        )

        # - Convert time column to datetime
        df["time"] = dd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S")

        return df

    ##------------------------------------------------------------------------.
    #### - Define glob pattern to search data files in raw_dir/data/<station_id>
    files_glob_pattern = "*.csv*"

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