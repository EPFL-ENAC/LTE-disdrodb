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
"""Check DISDRODB L0 issues processing."""

import os
from io import StringIO

import numpy as np
import pytest
import yaml

from disdrodb.issue.checks import (
    _check_time_period_nested_list_format,
    _check_timestep_datetime_accuracy,
    _check_timesteps_string,
    _get_issue_time_periods,
    _get_issue_timesteps,
    _is_numpy_array_datetime,
    _is_numpy_array_string,
    check_issue_dict,
    check_time_periods,
    check_timesteps,
)
from disdrodb.issue.reader import read_issue
from disdrodb.issue.writer import _write_issue, _write_issue_docs

####--------------------------------------------------------------------------.
#### Checks


def test__is_numpy_array_string():
    # Test string array
    arr = np.array(["foo", "bar"], dtype=np.str_)
    assert _is_numpy_array_string(arr) is True

    # Test unicode array
    arr = np.array(["foo", "bar"], dtype=np.unicode_)
    assert _is_numpy_array_string(arr) is True

    # Test nonstring array
    arr = np.array([1, 2, 3])
    assert _is_numpy_array_string(arr) is False

    # Test mixed type array
    arr = np.array(["foo", 1, 2.0], dtype=np.object_)
    assert _is_numpy_array_string(arr) is False


def test_check_issue_file():
    # function_return = check_issue_file()
    assert 1 == 1


####--------------------------------------------------------------------------.
#### Writer


def test_write_issue_docs():
    # Create a mock file object
    mock_file = StringIO()

    # Call the function under test
    _write_issue_docs(mock_file)

    # Get the written data from the mock file object
    written_data = mock_file.getvalue()

    # Check that the written data matches the expected output
    expected_output = """# This file is used to store timesteps/time periods with wrong/corrupted observation.
# The specified timesteps are dropped during the L0 processing.
# The time format used is the isoformat : YYYY-mm-dd HH:MM:SS.
# The 'timesteps' key enable to specify the list of timesteps to be discarded.
# The 'time_period' key enable to specify the time periods to be dropped.
# Example:
#
# timesteps:
# - 2018-12-07 14:15:00
# - 2018-12-07 14:17:00
# - 2018-12-07 14:19:00
# - 2018-12-07 14:25:00
# time_period:
# - ['2018-08-01 12:00:00', '2018-08-01 14:00:00']
# - ['2018-08-01 15:44:30', '2018-08-01 15:59:31']
# - ['2018-08-02 12:44:30', '2018-08-02 12:59:31'] \n
"""
    assert written_data == expected_output


def test__is_numpy_array_datetime():
    arr = np.array(["2022-01-01", "2022-01-02"], dtype="datetime64")
    assert _is_numpy_array_datetime(arr) is True

    arr = np.array([1, 2, 3])
    assert _is_numpy_array_datetime(arr) is False


def test__check_timestep_datetime_accuracy():
    timesteps = np.array(["2022-01-01T01:00:00", "2022-01-01T02:00:00"], dtype="datetime64[s]")
    assert np.array_equal(_check_timestep_datetime_accuracy(timesteps, unit="s"), timesteps)

    with pytest.raises(ValueError):
        timesteps = np.array(["2022-01-01", "2022-01-02"], dtype="datetime64[D]")
        _check_timestep_datetime_accuracy(timesteps, unit="s")


def test__check_timesteps_string():
    timesteps = ["2022-01-01 01:00:00", "2022-01-01 02:00:00"]
    expected_output = np.array(["2022-01-01T01:00:00", "2022-01-01T02:00:00"], dtype="datetime64[s]")
    assert np.array_equal(_check_timesteps_string(timesteps), expected_output)

    with pytest.raises(ValueError):
        timesteps = ["2022-01-01 01:00", "2022-01-01 02:00:00"]
        _check_timesteps_string(timesteps)


def test_check_timesteps():
    # Test None input
    assert check_timesteps(None) is None

    # Test string input
    timesteps_string = "2022-01-01 01:00:00"
    expected_output_string = np.array(["2022-01-01T01:00:00"], dtype="datetime64[s]")
    assert np.array_equal(check_timesteps(timesteps_string), expected_output_string)

    # Test list of string inputs
    timesteps_string_list = ["2022-01-01 01:00:00", "2022-01-01 02:00:00"]
    expected_output_string_list = np.array(["2022-01-01T01:00:00", "2022-01-01T02:00:00"], dtype="datetime64[s]")
    assert np.array_equal(check_timesteps(timesteps_string_list), expected_output_string_list)

    # Test datetime input
    timesteps_datetime = np.array(["2022-01-01T01:00:00", "2022-01-01T02:00:00"], dtype="datetime64[s]")
    expected_output_datetime = np.array(["2022-01-01T01:00:00", "2022-01-01T02:00:00"], dtype="datetime64[s]")
    assert np.array_equal(check_timesteps(timesteps_datetime), expected_output_datetime)

    # Test invalid input
    with pytest.raises(TypeError):
        check_timesteps(123)


def test_check_time_period_nested_list_format():
    # Test valid input
    time_periods_valid = [
        ["2022-01-01 01:00:00", "2022-01-01 02:00:00"],
        ["2022-01-02 01:00:00", "2022-01-02 02:00:00"],
    ]
    assert _check_time_period_nested_list_format(time_periods_valid) is None

    # Test invalid input type
    time_periods_invalid_type = "not a list"
    with pytest.raises(TypeError):
        _check_time_period_nested_list_format(time_periods_invalid_type)

    # Test invalid input length
    time_periods_invalid_length = [["2022-01-01 01:00:00", "2022-01-01 02:00:00"], ["2022-01-02 01:00:00"]]
    with pytest.raises(ValueError):
        _check_time_period_nested_list_format(time_periods_invalid_length)

    # Test invalid input element type
    time_periods_invalid_element_type = [["2022-01-01 01:00:00", 123], ["2022-01-02 01:00:00", "2022-01-02 02:00:00"]]
    assert _check_time_period_nested_list_format(time_periods_invalid_element_type) is None


def test_check_time_periods():
    # Valid input
    time_periods = [
        ["2022-01-01 01:00:00", "2022-01-01 02:00:00"],
        ["2022-01-02 01:00:00", "2022-01-02 02:00:00"],
    ]

    expected_result = [np.array(time_period, dtype="datetime64[s]") for time_period in time_periods]
    assert np.array_equal(check_time_periods(time_periods), expected_result)

    # None input
    assert check_time_periods(None) is None

    # Invalid input: invalid time period
    time_periods = [
        ["2022-01-01 01:00:00", "2022-01-01 02:00:00"],
        ["2022-01-02 01:00:00", "2021-01-02 02:00:00"],
    ]
    with pytest.raises(ValueError):
        check_time_periods(time_periods)

    # Invalid input: invalid format
    time_periods = [
        ["2022-01-01 01:00:00", "2022-01-01 02:00:00"],
        ["2022-01-02 01:00:00"],
    ]
    with pytest.raises(ValueError):
        check_time_periods(time_periods)


def test_get_issue_timesteps():
    # Test case 1: Valid timesteps
    time_periods = ["2022-01-01 01:00:00", "2022-01-01 02:00:00"]
    issue_dict = {"timesteps": time_periods}
    expected_result = [np.array(time_period, dtype="datetime64[s]") for time_period in time_periods]
    assert np.array_equal(_get_issue_timesteps(issue_dict), expected_result)


def test__get_issue_time_periods():
    # Test case 1: Valid time periods
    time_periods = [["2022-01-01 01:00:00", "2022-01-01 02:00:00"], ["2022-01-02 01:00:00", "2022-01-02 02:00:00"]]
    issue_dict = {"time_periods": time_periods}
    expected_result = [np.array(time_period, dtype="datetime64[s]") for time_period in time_periods]
    assert np.array_equal(_get_issue_time_periods(issue_dict), expected_result)

    # Test case 2: No time periods
    issue_dict = {}
    assert _get_issue_time_periods(issue_dict) is None


def test_check_issue_dict():
    # Test empty dictionary
    assert check_issue_dict({}) == {}

    # Test dictionary with invalid keys
    # with pytest.raises(ValueError):
    #     check_issue_dict({"foo": "bar"})

    # Test dictionary with valid keys and timesteps
    timesteps = ["2022-01-01 01:00:00", "2022-01-01 02:00:00"]

    issue_dict = {
        "timesteps": timesteps,
    }

    timesteps_datetime = np.array(timesteps, dtype="datetime64[s]")
    result = check_issue_dict(issue_dict)
    expected_result = {
        "timesteps": timesteps_datetime,
        "time_periods": None,
    }

    assert set(result.keys()) == set(expected_result.keys())

    # Test timesteps kees
    assert np.array_equal(result["timesteps"], expected_result["timesteps"])

    # Test invalid keys
    issue_dict = {"timesteps": timesteps, "invalid_key": "invalid_value"}
    with pytest.raises(ValueError):
        check_issue_dict(issue_dict)


def test_write_issue(tmpdir):
    """Test the _write_issue function."""
    # Define test inputs
    filepath = os.path.join(tmpdir, "test_yml")
    timesteps = np.array([0, 1, 2])
    time_periods = np.array([[0, 1], [2, 3]])

    # Call function
    _write_issue(filepath, timesteps=timesteps, time_periods=time_periods)

    # Load YAML file
    with open(filepath) as f:
        issue_dict = yaml.load(f, Loader=yaml.FullLoader)

    # Check the issue dictionary
    assert isinstance(issue_dict, dict)
    assert len(issue_dict) == 2
    assert issue_dict.keys() == {"timesteps", "time_periods"}
    assert np.array_equal(issue_dict["timesteps"], timesteps.astype(str).tolist())
    assert np.array_equal(issue_dict["time_periods"], time_periods.astype(str).tolist())

    # Test dictionary with valid keys and timesteps
    timesteps = ["2022-01-01 01:00:00", "2022-01-01 02:00:00"]

    issue_dict = {
        "timesteps": timesteps,
    }

    _write_issue(filepath, timesteps=np.array(timesteps), time_periods=None)

    result = read_issue(filepath)

    timesteps_datetime = np.array(timesteps, dtype="datetime64[s]")
    expected_result = {
        "timesteps": timesteps_datetime,
        "time_periods": None,
    }
    # assert np.array_equal(result,expected_result)
    assert set(result.keys()) == set(expected_result.keys())
    assert np.array_equal(result["timesteps"], expected_result["timesteps"])