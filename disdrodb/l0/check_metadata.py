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
"""Check metadata."""

import os
from typing import Union

from disdrodb.api.metadata import get_list_metadata, read_station_metadata
from disdrodb.configs import get_base_dir
from disdrodb.l0.io import (
    _infer_campaign_name_from_path,
    _infer_data_source_from_path,
)
from disdrodb.l0.l0_reader import _check_metadata_reader
from disdrodb.l0.metadata import (
    _check_metadata_campaign_name,
    _check_metadata_data_source,
    _check_metadata_keys,
    _check_metadata_sensor_name,
    _check_metadata_station_name,
    check_metadata_compliance,
)
from disdrodb.utils.yaml import read_yaml

#### --------------------------------------------------------------------------.
#### Metadata Archive Missing Information


def _check_lonlat_type(longitude, latitude):
    # Check type validity
    if isinstance(longitude, str):
        raise TypeError("longitude is not defined as numeric.")
    if isinstance(latitude, str):
        raise TypeError("latitude is not defined as numeric.")
    # Check is not none
    if isinstance(longitude, type(None)) or isinstance(latitude, type(None)):
        raise ValueError("Unspecified longitude and latitude coordinates.")


def _check_lonlat_validity(longitude, latitude):
    if longitude == -9999 or latitude == -9999:
        raise ValueError("Missing lat lon coordinates (-9999).")
    elif longitude > 180 or longitude < -180:
        raise ValueError("Invalid longitude (outside [-180, 180])")
    elif latitude > 90 or latitude < -90:
        raise ValueError("Invalid latitude (outside [-90, 90])")
    else:
        pass


def check_metadata_geolocation(metadata) -> None:
    """Identify metadata with missing or wrong geolocation."""
    # Get longitude, latitude and platform type
    longitude = metadata.get("longitude")
    latitude = metadata.get("latitude")
    platform_type = metadata.get("platform_type")
    # Check type validity
    _check_lonlat_type(longitude=longitude, latitude=latitude)
    # Check value validity
    # - If mobile platform
    if platform_type == "mobile":
        if longitude != -9999 or latitude != -9999:
            raise ValueError("For mobile platform_type, specify latitude and longitude -9999")
    # - If fixed platform
    else:
        _check_lonlat_validity(longitude=longitude, latitude=latitude)
    return None


def identify_missing_metadata_coords(metadata_fpaths: str) -> None:
    """Identify missing coordinates.

    Parameters
    ----------
    metadata_fpaths : str
        Input YAML file path.

    Raises
    ------
    TypeError
        Error if latitude or longitude coordinates are not present or are wrongly formatted.

    """
    for fpath in metadata_fpaths:
        metadata = read_yaml(fpath)
        check_metadata_geolocation(metadata)
    return None


def identify_empty_metadata_keys(metadata_fpaths: list, keys: Union[str, list]) -> None:
    """Identify empty metadata keys.

    Parameters
    ----------
    metadata_fpaths : str
        Input YAML file path.
    keys : Union[str,list]
        Attributes to verify the presence.
    """

    if isinstance(keys, str):
        keys = [keys]

    for fpath in metadata_fpaths:
        for key in keys:
            metadata = read_yaml(fpath)
            if len(str(metadata.get(key, ""))) == 0:  # ensure is string to avoid error
                print(f"Empty {key} at: ", fpath)
    return None


def get_archive_metadata_key_value(key: str, return_tuple: bool = True, base_dir: str = None):
    """Return the values of a metadata key for all the archive.

    Parameters
    ----------
    base_dir : str
        Path to the disdrodb directory.
    key : str
        Metadata key.
    return_tuple : bool, optional
       If True, returns a tuple of values with station, campaign and data source name.
       If False, returns a list of values without station, campaign and data source name.
       The default is True.
    base_dir : str (optional)
       Base directory of DISDRODB. Format: <...>/DISDRODB
       If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    list or tuple
        List or tuple of values of the metadata key.
    """
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    list_info = []
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")
        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        value = metadata[key]
        info = (data_source, campaign_name, station_name, value)
        list_info.append(info)
    if not return_tuple:
        list_info = [info[3] for info in list_info]
    return list_info


#### --------------------------------------------------------------------------.
#### Metadata Archive Checks


def check_archive_metadata_keys(base_dir: str = None) -> bool:
    """Check that all metadata files have valid keys

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_keys(metadata)
        except Exception as e:
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
            is_valid = False

    return is_valid


def check_archive_metadata_campaign_name(base_dir: str = None) -> bool:
    """Check metadata campaign_name.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_campaign_name(metadata, expected_name=campaign_name)
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_data_source(base_dir: str = None) -> bool:
    """Check metadata data_source.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_data_source(metadata, expected_name=data_source)
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_sensor_name(base_dir: str = None) -> bool:
    """Check metadata sensor name.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_sensor_name(metadata)
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_station_name(base_dir: str = None) -> bool:
    """Check metadata station name.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_station_name(metadata, expected_name=station_name)
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_reader(base_dir: str = None) -> bool:
    """Check if the reader key is available and there is the associated reader.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """

    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            _check_metadata_reader(metadata)
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_compliance(base_dir: str = None):
    """Check the archive metadata compliance.

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")
        try:
            check_metadata_compliance(
                base_dir=base_dir,
                data_source=data_source,
                campaign_name=campaign_name,
                station_name=station_name,
            )
        except Exception as e:
            is_valid = False
            print(f"Error for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid


def check_archive_metadata_geolocation(base_dir: str = None):
    """Check the metadata files have missing or wrong geolocation..

    Parameters
    ----------
    base_dir : str (optional)
        Base directory of DISDRODB. Format: <...>/DISDRODB
        If None (the default), the disdrodb config variable 'dir' is used.

    Returns
    -------
    bool
        If the check succeeds, the result is True, and if it fails, the result is False.
    """
    is_valid = True
    base_dir = get_base_dir(base_dir)
    list_metadata_paths = get_list_metadata(
        base_dir=base_dir, data_sources=None, campaign_names=None, station_names=None, with_stations_data=False
    )
    for fpath in list_metadata_paths:
        data_source = _infer_data_source_from_path(fpath)
        campaign_name = _infer_campaign_name_from_path(fpath)
        station_name = os.path.basename(fpath).replace(".yml", "")

        metadata = read_station_metadata(
            base_dir=base_dir,
            product_level="RAW",
            data_source=data_source,
            campaign_name=campaign_name,
            station_name=station_name,
        )
        try:
            check_metadata_geolocation(metadata)
        except Exception as e:
            is_valid = False
            print(f"Missing information for {data_source} {campaign_name} {station_name}.")
            print(f"The error is: {e}.")
    return is_valid
