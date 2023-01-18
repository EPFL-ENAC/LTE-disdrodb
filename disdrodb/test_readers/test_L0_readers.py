import os
import shutil
import requests
import subprocess
import zipfile
import glob
import numpy as np
import xarray as xr
from netCDF4 import Dataset
import pytest


from disdrodb.L0.L0_processing import run_reader


# Define paths
PATH_FOLDER_ROOT = os.path.dirname(os.path.realpath(__file__))
NAME_FOLDER_TEST_RESULTS = "temp"
NAME_FOLDER_TEST_GROUND_TRUTH = "test_ressources_ground_truth"
NAME_FOLDER_RAW_DATA = "test_ressources_raw_data"


def run_reader_on_test_data(data_source: str, campaign_name: str) -> None:
    """Run reader on test data.


    Parameters
    ----------
    data_source : str
        Data source.

    campaign_name : str
        Name of the campaign.

    """

    raw_dir = os.path.join(
        PATH_FOLDER_ROOT,
        NAME_FOLDER_RAW_DATA,
        "L0",
        "readers",
        "DISDRODB",
        "Raw",
        data_source,
        campaign_name,
    )
    if not os.path.exists(raw_dir):
        raise ValueError(f"{raw_dir} does not exist")

    processed_dir = os.path.join(
        PATH_FOLDER_ROOT,
        NAME_FOLDER_TEST_RESULTS,
        "DISDRODB",
        "Processed",
        data_source,
        campaign_name,
    )
    l0a_processing = True
    l0b_processing = True
    keep_l0a = True
    force = True
    verbose = False
    debugging_mode = True
    lazy = True
    single_netcdf = True

    run_reader(
        data_source,
        campaign_name,
        raw_dir,
        processed_dir,
        l0a_processing,
        l0b_processing,
        keep_l0a,
        force,
        verbose,
        debugging_mode,
        lazy,
        single_netcdf,
    )


def are_netcdf_identical(dataset_1: Dataset, dataset_2: Dataset) -> bool:

    """Check if two NetCDF are identical.


    Parameters
    ----------
    dataset_1 : Dataset
        First NetCDF
    dataset_2 : Dataset
        Second NetCDF

    Returns
    -------
    bool
        True if identical,
        False if not indentical
    """

    is_identical = True

    # Check dimension keys
    if is_identical and dataset_1.dimensions.keys() != dataset_2.dimensions.keys():
        is_identical = False

    # Check variables keys
    if is_identical and dataset_1.variables.keys() != dataset_2.variables.keys():
        is_identical = False

    # Check dimension content
    if is_identical:
        for dimension_name in dataset_2.dimensions.keys():
            dimension_result = dataset_1.variables[dimension_name][:]
            dimension_ground_thruth = dataset_2.variables[dimension_name][:]
            if not np.array_equal(dimension_ground_thruth, dimension_result):
                is_identical = False
                print(f"The dimension '{dimension_name}' does not match.")

    # Check variable content
    if is_identical:
        for variable_name in dataset_2.variables.keys():
            variable_result = dataset_1.variables[variable_name][:]
            variable_ground_truth = dataset_2.variables[variable_name][:]
            if not np.array_equal(variable_result, variable_ground_truth):
                is_identical = False
                print(f"The variable '{variable_name}' does not match")

    return is_identical


def is_reader_results_similar_to_ground_truth(
    data_source: str, campaign_name: str
) -> bool:
    """Test if the reader execution returns the same result as the ground truth.

    Parameters
    ----------
    data_source : str
        Data source.

    campaign_name : str
        Name of the campaign.


    Returns
    -------
    bool
        True if reader execution returns same result as ground truth
        False if the results of the reader execution diverge from the ground truth.
    """

    ground_truth_folder = os.path.join(
        PATH_FOLDER_ROOT,
        NAME_FOLDER_TEST_GROUND_TRUTH,
        "DISDRODB",
        "Processed",
        data_source,
        campaign_name,
        "L0B",
    )
    list_of_ground_truth_files_paths = glob.glob(
        os.path.join(ground_truth_folder, "*", "*.nc")
    )

    result_folder = os.path.join(
        PATH_FOLDER_ROOT,
        NAME_FOLDER_TEST_RESULTS,
        "DISDRODB",
        "Processed",
        data_source,
        campaign_name,
        "L0B",
    )
    list_of_test_result_files_paths = glob.glob(
        os.path.join(result_folder, "*", "*.nc")
    )

    is_reader_result_similar_to_ground_truth = True

    for ground_truth_file_path in list_of_ground_truth_files_paths:
        groud_truth_file_name = os.path.basename(ground_truth_file_path)
        ground_truth_station_name = os.path.basename(
            os.path.dirname(ground_truth_file_path)
        )
        for result_file_path in list_of_test_result_files_paths:
            result_file_name = os.path.basename(result_file_path)
            result_station_name = os.path.basename(os.path.dirname(result_file_path))
            if ground_truth_station_name == result_station_name:
                # Load datasets
                dataset_1 = Dataset(ground_truth_file_path)
                dataset_2 = Dataset(result_file_path)
                if not are_netcdf_identical(dataset_1, dataset_2):

                    is_reader_result_similar_to_ground_truth = False
                    print(f"{result_file_name} does not match {groud_truth_file_name}")

    return is_reader_result_similar_to_ground_truth


def get_list_of_reader_to_be_tested_from_row_folder() -> dict:
    """This function parses the test data sample folder to create a dictionary gathering the data source name and campaign name.

    Returns
    -------
    dict
        Dictionary with data source name and campaign name.
    """
    folder_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        NAME_FOLDER_RAW_DATA,
        "L0",
        "readers",
        "DISDRODB",
        "Raw",
    )
    index_raw_folder = os.path.normpath(folder_path).split(os.sep).index("Raw")
    number_of_element_until_data_folder = index_raw_folder + 3

    list_files_paths = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(folder_path)
        for f in filenames
    ]

    temp_dict = {}

    for i in list_files_paths:
        list_of_path_elements = os.path.normpath(i).split(os.sep)
        if list_of_path_elements[number_of_element_until_data_folder] == "data":

            data_source_name = list_of_path_elements[index_raw_folder + 1]
            campaign_name = list_of_path_elements[index_raw_folder + 2]

            if len(list_of_path_elements) == index_raw_folder + 6:  # has data file
                if not temp_dict.get(data_source_name):
                    temp_dict[data_source_name] = []

                if campaign_name not in temp_dict[data_source_name]:
                    temp_dict[data_source_name].append(campaign_name)

    return temp_dict


def reader_to_be_tested() -> list:
    """Set the tests folder and return the list of tests to be executed.

    Returns
    -------
    list
        List of tests to be executed.
    """

    temp_folder = os.path.join(PATH_FOLDER_ROOT, NAME_FOLDER_TEST_RESULTS)
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.mkdir(temp_folder)

    # get the list of reader to be tested
    list_of_reader_to_be_tested_from_row_folder = (
        get_list_of_reader_to_be_tested_from_row_folder()
    )

    list_of_reader_to_be_tested = []

    for (
        data_source_name,
        list_of_campaign,
    ) in list_of_reader_to_be_tested_from_row_folder.items():
        for campaign_name in list_of_campaign:
            list_of_reader_to_be_tested.append((data_source_name, campaign_name))

    return list_of_reader_to_be_tested


@pytest.mark.parametrize("reader_to_be_tested", reader_to_be_tested())
def test_reader_full_execution(reader_to_be_tested: tuple) -> None:
    """Test the reader.

    Parameters
    ----------
    list_of_reader_to_be_tested : list
        List of reader to be tested.
    """

    data_source_name = reader_to_be_tested[0]
    campaign_name = reader_to_be_tested[1]
    msg = f"Start test for data source '{data_source_name}' and campaign '{campaign_name}' "
    run_reader_on_test_data(data_source_name, campaign_name)
    result = is_reader_results_similar_to_ground_truth(data_source_name, campaign_name)
    assert result
    msg = (
        f"End test for data source '{data_source_name}' and campaign '{campaign_name}' "
    )
    print(msg)
