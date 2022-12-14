import os
import shutil

SOURCE_ROOT_FOLDER = "X:\\ltenas3\\data\\DISDRODB\\Raw"
DESTINATION_ROOT_FOLDER = "C:\projects\\LTE-disdrodb-data\\DISDRODB\\Raw"


def get_list_file_paths_to_load_to_repo(raw_folder_path: str) -> list:
    """List of the file to upload to zenodo

    Parameters
    ----------
    raw_folder_path : str
        roo folder path

    Returns
    -------
    list
        List of file paths
    """
    result = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(raw_folder_path)
        for f in filenames
    ]

    list_of_file_to_upload = list()

    for i in result:
        list_of_path_elements = os.path.normpath(i).split(os.sep)
        data_source = list_of_path_elements[5]
        campagn_name = list_of_path_elements[6]
        data_type = list_of_path_elements[7]

        file_name_part = list_of_path_elements[8:]

        if data_type in ["issue", "metadata"]:
            print(i)
            path_data_type = os.path.join(
                DESTINATION_ROOT_FOLDER, data_source, campagn_name, data_type
            )
            if not os.path.exists(path_data_type):
                os.makedirs(path_data_type)
            path_file = os.path.join(path_data_type, *file_name_part)
            shutil.copyfile(i, path_file)


get_list_file_paths_to_load_to_repo(SOURCE_ROOT_FOLDER)
