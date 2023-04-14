import pytest
import pandas as pd
from disdrodb.l0 import check_standards
import random
import numpy as np


def test_check_valid_range():
    # Test case 1: All columns within range
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [0.5, 1.2, 2.7, 3.8]})
    dict_data_range = {"col1": [0, 5], "col2": [0, 4]}
    assert check_standards._check_valid_range(df, dict_data_range) is None

    # Test case 2: Some columns outside range
    df = pd.DataFrame({"col1": [1, 2, 10, 4], "col2": [0.5, 5.2, 2.7, 3.8]})
    dict_data_range = {"col1": [0, 5], "col2": [0, 4]}
    with pytest.raises(ValueError, match=r".*Columns \['col1', 'col2'\] has values outside the expected data range.*"):
        check_standards._check_valid_range(df, dict_data_range)

    # Test case 3: Empty dataframe
    df = pd.DataFrame()
    dict_data_range = {"col1": [0, 5], "col2": [0, 4]}
    assert check_standards._check_valid_range(df, dict_data_range) is None

    # Test case 4: Non-existing columns
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [0.5, 1.2, 2.7, 3.8]})
    dict_data_range = {"col1": [0, 5], "col3": [0, 4]}
    assert check_standards._check_valid_range(df, dict_data_range) is None


def test_check_valid_values():
    # Test case 1: All columns have valid values
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [1, 2, 3, 4]})
    dict_valid_values = {"col1": [1, 2, 3, 4], "col2": [1, 2, 3, 4]}
    assert check_standards._check_valid_values(df, dict_valid_values) is None

    # Test case 2: Some columns have invalid values
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [1, 5, 3, 4]})
    dict_valid_values = {"col1": [1, 2, 3, 4], "col2": [1, 2, 3, 4]}
    with pytest.raises(ValueError):
        check_standards._check_valid_values(df, dict_valid_values)

    # Test case 3: Empty dataframe
    df = pd.DataFrame()
    dict_valid_values = {"col1": [1, 2, 3, 4], "col2": [1, 2, 3, 4]}
    assert check_standards._check_valid_values(df, dict_valid_values) is None

    # Test case 4: Non-existing columns
    df = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [1, 2, 3, 4]})
    dict_valid_values = {"col1": [1, 2, 3, 4], "col3": [1, 2, 3, 4]}
    assert check_standards._check_valid_values(df, dict_valid_values) is None


def test_check_raw_fields_available():
    # Test case 1: Missing 'raw_drop_number' column
    df = pd.DataFrame({"other_column": [1, 2, 3]})
    sensor_name = "some_sensor_type"
    with pytest.raises(ValueError):
        check_standards._check_raw_fields_available(df, sensor_name)

    # Test case 2: All required columns present
    from disdrodb.l0.standards import available_sensor_name, get_raw_array_nvalues

    available_sensor_name = available_sensor_name()
    sensor_name = random.choice(available_sensor_name)
    n_bins_dict = get_raw_array_nvalues(sensor_name=sensor_name)
    raw_vars = np.array(list(n_bins_dict.keys()))
    dict_data = {i: [1, 2] for i in raw_vars}
    df = pd.DataFrame.from_dict(dict_data)

    assert check_standards._check_raw_fields_available(df, sensor_name) is None


def test_check_sensor_name():
    sensor_name = "wrong_sensor_name"

    # Test with an unknown device
    with pytest.raises(ValueError):
        check_standards.check_sensor_name(sensor_name)

    # Test with a woronf type
    with pytest.raises(TypeError):
        check_standards.check_sensor_name(123)


def test_check_l0a_column_names(capsys):
    from disdrodb.l0.standards import available_sensor_name, get_sensor_variables

    available_sensor_name = available_sensor_name()
    sensor_name = random.choice(available_sensor_name)

    # Test 1 : All columns are present
    list_column_names = get_sensor_variables(sensor_name) + ["time", "latitude", "longitude"]
    dict_data = {i: [1, 2] for i in list_column_names}
    df = pd.DataFrame.from_dict(dict_data)
    # assert check_standards.check_l0a_column_names(df, sensor_name=sensor_name) is None

    # Test 2 : Missing columns time
    list_column_names = get_sensor_variables(sensor_name) + ["latitude", "longitude"]
    dict_data = {i: [1, 2] for i in list_column_names}
    df = pd.DataFrame.from_dict(dict_data)
    with pytest.raises(ValueError):
        check_standards.check_l0a_column_names(df, sensor_name=sensor_name) is None

    # Test 3 : fake panda dataframe
    data = {"wrong_column_name": ["John", "Jane", "Bob", "Sara"]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError):
        check_standards.check_l0a_column_names(df, sensor_name=sensor_name)

    # Test 4 : Missing columns latitude
    list_column_names = get_sensor_variables(sensor_name) + ["time", "longitude"]
    dict_data = {i: [1, 2] for i in list_column_names}
    df = pd.DataFrame.from_dict(dict_data)
    check_standards.check_l0a_column_names(df, sensor_name=sensor_name)
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == " - The L0A dataframe has column 'latitude'. "
        "This should be included only if the sensor is moving. "
        "Otherwise, specify the 'latitude' in the metadata !"
    )


def test_check_l0b_standards():
    assert check_standards.test_check_l0b_standards() is None
