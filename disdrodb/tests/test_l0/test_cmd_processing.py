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
"""Test DISDRODB L0 processing commands."""

import glob
import os
import shutil

import pytest
from click.testing import CliRunner

from disdrodb import __root_path__

RAW_DIR = os.path.join(__root_path__, "disdrodb", "tests", "data", "check_readers", "DISDRODB")
DATA_SOURCE = "EPFL"
CAMPAIGN_NAME = "PARSIVEL_2007"
STATION_NAME = "10"


@pytest.fixture
def remove_processed_folder(request: list) -> None:
    path_processed_folder = os.path.join(RAW_DIR, "Processed")
    if os.path.exists(path_processed_folder):
        shutil.rmtree(path_processed_folder)
    yield
    if os.path.exists(path_processed_folder):
        shutil.rmtree(path_processed_folder)


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_disdrodb_run_l0a_station(remove_processed_folder):
    """Test the disdrodb_run_l0a_station command."""

    from disdrodb.l0.scripts.disdrodb_run_l0a_station import disdrodb_run_l0a_station

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0a_station, [DATA_SOURCE, CAMPAIGN_NAME, STATION_NAME, "--base_dir", RAW_DIR])
    list_of_l0a = glob.glob(
        os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0A", STATION_NAME, "*.parquet")
    )
    assert len(list_of_l0a) > 0


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_disdrodb_run_l0a(remove_processed_folder):
    """Test the disdrodb_run_l0a command."""

    from disdrodb.l0.scripts.disdrodb_run_l0a import disdrodb_run_l0a

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0a, ["--base_dir", RAW_DIR])
    list_of_l0a = glob.glob(
        os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0A", STATION_NAME, "*.parquet")
    )
    assert len(list_of_l0a) > 0


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_disdrodb_run_l0b_station(remove_processed_folder):
    """Test the disdrodb_run_l0b_station command."""
    from disdrodb.l0.scripts.disdrodb_run_l0a_station import disdrodb_run_l0a_station

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0a_station, [DATA_SOURCE, CAMPAIGN_NAME, STATION_NAME, "--base_dir", RAW_DIR])

    from disdrodb.l0.scripts.disdrodb_run_l0b_station import disdrodb_run_l0b_station

    runner.invoke(disdrodb_run_l0b_station, [DATA_SOURCE, CAMPAIGN_NAME, STATION_NAME, "--base_dir", RAW_DIR])

    list_of_l0b = glob.glob(os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0B", STATION_NAME, "*.nc"))
    assert len(list_of_l0b) > 0


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_disdrodb_run_l0_station(remove_processed_folder):
    """Test the disdrodb_run_l0_station command."""

    from disdrodb.l0.scripts.disdrodb_run_l0_station import disdrodb_run_l0_station

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0_station, [DATA_SOURCE, CAMPAIGN_NAME, STATION_NAME, "--base_dir", RAW_DIR])

    list_of_l0b = glob.glob(os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0B", STATION_NAME, "*.nc"))
    assert len(list_of_l0b) > 0


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_disdrodb_run_l0b(remove_processed_folder):
    """Test the disdrodb_run_l0b command."""

    from disdrodb.l0.scripts.disdrodb_run_l0a import disdrodb_run_l0a

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0a, ["--base_dir", RAW_DIR])

    from disdrodb.l0.scripts.disdrodb_run_l0b import disdrodb_run_l0b

    runner.invoke(disdrodb_run_l0b, ["--base_dir", RAW_DIR])
    list_of_l0b = glob.glob(os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0B", STATION_NAME, "*.nc"))
    assert len(list_of_l0b) > 0


@pytest.mark.parametrize("remove_processed_folder", [()], indirect=True)
def test_full_disdrodb_run_l0(remove_processed_folder):
    """Test the disdrodb_run_l0b command."""

    from disdrodb.l0.scripts.disdrodb_run_l0 import disdrodb_run_l0

    runner = CliRunner()
    runner.invoke(disdrodb_run_l0, ["--base_dir", RAW_DIR])

    list_of_l0b = glob.glob(os.path.join(RAW_DIR, "Processed", DATA_SOURCE, CAMPAIGN_NAME, "L0B", STATION_NAME, "*.nc"))
    assert len(list_of_l0b) > 0
