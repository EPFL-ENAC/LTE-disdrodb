#!/usr/bin/env python3

# -----------------------------------------------------------------------------.
# Copyright (c) 2021-2023 DISDRODB developers
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
"""Retrieve file information from DISDRODB products file names and filepaths."""

import os
from pathlib import Path

import numpy as np
from trollsift import Parser

####---------------------------------------------------------------------------
########################
#### FNAME PATTERNS ####
########################
DISDRODB_FNAME_PATTERN = (
    "{product:s}.{campaign_name:s}.{station_name:s}.s{start_time:%Y%m%d%H%M%S}.e{end_time:%Y%m%d%H%M%S}"
    ".{version:s}.{data_format:s}"
)

####---------------------------------------------------------------------------.
##########################
#### Filename parsers ####
##########################


def _parse_fname(fname):
    """Parse the filename with trollsift."""
    # Retrieve information from filename
    p = Parser(DISDRODB_FNAME_PATTERN)
    info_dict = p.parse(fname)
    return info_dict


def _get_info_from_filename(fname):
    """Retrieve file information dictionary from filename."""
    # Try to parse the filename
    try:
        info_dict = _parse_fname(fname)
    except ValueError:
        raise ValueError(f"{fname} can not be parsed. Report the issue.")
    # Return info dictionary
    return info_dict


def get_info_from_filepath(fpath):
    """Retrieve file information dictionary from filepath."""
    if not isinstance(fpath, str):
        raise TypeError("'fpath' must be a string.")
    fname = os.path.basename(fpath)
    return _get_info_from_filename(fname)


def get_key_from_filepath(fpath, key):
    """Extract specific key information from a list of filepaths."""
    value = get_info_from_filepath(fpath)[key]
    return value


def get_key_from_filepaths(fpaths, key):
    """Extract specific key information from a list of filepaths."""
    if isinstance(fpaths, str):
        fpaths = [fpaths]
    return [get_key_from_filepath(fpath, key=key) for fpath in fpaths]


####--------------------------------------------------------------------------.
###################################
#### DISDRODB File Information ####
###################################


def _get_version_from_filepath(filepath):
    version = get_key_from_filepath(filepath, key="version")
    return version


def get_version_from_filepaths(filepaths):
    if isinstance(filepaths, str):
        filepaths = [filepaths]
    list_version = [_get_version_from_filepath(fpath) for fpath in filepaths]
    return list_version


def get_campaign_name_from_filepaths(filepaths):
    list_id = get_key_from_filepaths(filepaths, key="campaign_name")
    return list_id


def get_station_name_from_filepaths(filepaths):
    list_id = get_key_from_filepaths(filepaths, key="station_name")
    return list_id


def get_product_from_filepaths(filepaths):
    list_id = get_key_from_filepaths(filepaths, key="product")
    return list_id


def get_start_time_from_filepaths(filepaths):
    list_start_time = get_key_from_filepaths(filepaths, key="start_time")
    return list_start_time


def get_end_time_from_filepaths(filepaths):
    list_end_time = get_key_from_filepaths(filepaths, key="end_time")
    return list_end_time


def get_start_end_time_from_filepaths(filepaths):
    list_start_time = get_key_from_filepaths(filepaths, key="start_time")
    list_end_time = get_key_from_filepaths(filepaths, key="end_time")
    return np.array(list_start_time), np.array(list_end_time)


####--------------------------------------------------------------------------.
###################################
#### DISDRODB Tree Components  ####
###################################


def infer_disdrodb_tree_path_components(path: str) -> list:
    """Return a list with the component of the disdrodb_path.

    Parameters
    ----------
    path : str
        `path` can be a campaign_dir ('raw_dir' or 'processed_dir'), or a DISDRODB file path.

    Returns
    -------
    list
        Path element of the DISDRODB archive.
        Format: [<base_dir>, <Raw or Processed>, <DATA_SOURCE>, ...]
    """
    # Retrieve path elements (os-specific)
    p = Path(path)
    list_path_elements = [str(part) for part in p.parts]
    # Retrieve where "DISDRODB" directory occurs
    idx_occurrence = np.where(np.isin(list_path_elements, "DISDRODB"))[0]
    # If DISDRODB directory not present, raise error
    if len(idx_occurrence) == 0:
        raise ValueError(f"The DISDRODB directory is not present in the path '{path}'")
    # Find the rightermost occurrence
    right_most_occurrence = max(idx_occurrence)
    # Define base_dir and tree components
    base_dir = os.path.join(*list_path_elements[: right_most_occurrence + 1])
    tree_components = list_path_elements[right_most_occurrence + 1 :]
    # Return components
    components = [base_dir] + tree_components
    return components


def infer_disdrodb_tree_path(path: str) -> str:
    """Return the directory tree path from the base_dir directory.

    Current assumption: no data_source, campaign_name, station_name or file contain the word DISDRODB!

    Parameters
    ----------
    path : str
        `path` can be a campaign_dir ('raw_dir' or 'processed_dir'), or a DISDRODB file path.

    Returns
    -------
    str
        Path inside the DISDRODB archive.
        Format: DISDRODB/<Raw or Processed>/<DATA_SOURCE>/...
    """
    components = infer_disdrodb_tree_path_components(path=path)
    tree_fpath = os.path.join("DISDRODB", *components[1:])
    return tree_fpath


def infer_base_dir_from_fpath(path: str) -> str:
    """Return the disdrodb base directory from a file or directory path.

    Assumption: no data_source, campaign_name, station_name or file contain the word DISDRODB!

    Parameters
    ----------
    path : str
        `path` can be a campaign_dir ('raw_dir' or 'processed_dir'), or a DISDRODB file path.

    Returns
    -------
    str
        Path of the DISDRODB directory.
    """
    return infer_disdrodb_tree_path_components(path=path)[0]


def infer_campaign_name_from_path(path: str) -> str:
    """Return the campaign name from a file or directory path.

    Assumption: no data_source, campaign_name, station_name or file contain the word DISDRODB!

    Parameters
    ----------
    path : str
       `path` can be a campaign_dir ('raw_dir' or 'processed_dir'), or a DISDRODB file path.

    Returns
    -------
    str
        Name of the campaign.
    """
    list_path_elements = infer_disdrodb_tree_path_components(path)
    if len(list_path_elements) <= 3:
        raise ValueError(f"Impossible to determine campaign_name from {path}")
    campaign_name = list_path_elements[3]
    return campaign_name


def infer_data_source_from_path(path: str) -> str:
    """Return the data_source from a file or directory path.

    Assumption: no data_source, campaign_name, station_name or file contain the word DISDRODB!

    Parameters
    ----------
    path : str
       `path` can be a campaign_dir ('raw_dir' or 'processed_dir'), or a DISDRODB file path.

    Returns
    -------
    str
        Name of the data source.
    """
    list_path_elements = infer_disdrodb_tree_path_components(path)
    if len(list_path_elements) <= 2:
        raise ValueError(f"Impossible to determine data_source from {path}")
    data_source = list_path_elements[2]
    return data_source


####--------------------------------------------------------------------------.
