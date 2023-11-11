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
"""Issue YAML File Writer."""

import logging
import yaml


logger = logging.getLogger(__name__)


def _write_issue_docs(f):
    """Provide template for issue.yml"""
    f.write("""# This file is used to store timesteps/time periods with wrong/corrupted observation.
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
""")
    return None


def _write_issue(filepath: str, timesteps: list = None, time_periods: list = None) -> None:
    """Write the issue YAML file.

    Parameters
    ----------
    filepath : str
        Filepath of the issue YAML to write.
    timesteps : list, optional
        List of timesteps (to be dropped in L0 processing).
        The default is None.
    time_periods : list, optional
        A list of time periods (to be dropped in L0 processing).
        The default is None.
    """
    # Preprocess timesteps and time_periods (to plain list of strings)
    if timesteps is not None:
        timesteps = timesteps.astype(str).tolist()

    if time_periods is not None:
        new_periods = []
        for time_period in time_periods:
            new_periods.append(time_period.astype(str).tolist())
        time_periods = new_periods

    # Write the issue YAML file
    logger.info(f"Creating issue YAML file at {filepath}")
    with open(filepath, "w") as f:
        # Write the docs for the issue.yml
        _write_issue_docs(f)

        # Write timesteps if provided
        if timesteps is not None:
            timesteps_dict = {"timesteps": timesteps}
            yaml.dump(timesteps_dict, f, default_flow_style=False)

        # Write time_periods if provided
        if time_periods is not None:
            time_periods_dict = {"time_periods": time_periods}
            yaml.dump(time_periods_dict, f, default_flow_style=None)
    return None


def write_issue_dict(filepath: str, issue_dict: dict) -> None:
    """Write the issue YAML file.

    Parameters
    ----------
    filepath : str
        Filepath of the issue YAML to write.
    issue_dict : dict
        Issue dictionary
    """
    _write_issue(
        filepath=filepath,
        timesteps=issue_dict.get("timesteps", None),
        time_periods=issue_dict.get("time_periods", None),
    )


def write_default_issue(filepath: str) -> None:
    """Write an empty issue YAML file.

    Parameters
    ----------
    filepath : str
        Filepath of the issue YAML to write.
    """
    _write_issue(filepath=filepath)
    return None
