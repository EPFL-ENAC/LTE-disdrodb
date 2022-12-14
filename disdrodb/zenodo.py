import os
import json
import uuid
import logging
from datetime import datetime
import pynodo
import time

# Instructions :

# 1. log in zenodo
# 2. start an edit session (new version)
# 3. copy the session id from the url
# 4. paste it under "DEPO_ID"
# 5. Run this Code
# 6. Publish the session


ACCESS_TOKEN = "AedArn7meXsxQlfba0WmxBdiJS2mLOOjpQ9cxdkUe7OZp9es04wSty3PY0z9"
DEPO_ID = "7431056"

path_folder_in = "X:\\ltenas8\\data\\DISDRODB\\Raw\\\EPFL\\PARSIVEL_2007"
path_folder_out_raw = "C:\projects\LTE-disdrodb-data\DISDRODB\Raw"
extension_to_remove = [".log"]

logging.basicConfig(
    filename=os.path.join(path_folder_out_raw, "upload_to_zenodo.log"),
    filemode="w",
    format="%(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_list_file_paths_to_load_to_zenodo(folder_path: str) -> list:
    """List of the file to upload to zenodo

    Parameters
    ----------
    folder_path : str
        roo folder path

    Returns
    -------
    list
        List of file paths
    """
    result = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(folder_path)
        for f in filenames
    ]

    list_of_file_to_upload = list()

    index_raw_folder = os.path.normpath(path_folder_in).split(os.sep).index("Raw")
    number_of_element_until_data_folder = index_raw_folder + 3

    for i in result:
        list_of_path_elements = os.path.normpath(i).split(os.sep)
        if (
            list_of_path_elements[number_of_element_until_data_folder] == "data"
            and not list_of_path_elements[-1] == "urls.txt"
            and not i.endswith(tuple(extension_to_remove))
        ):
            list_of_file_to_upload.append(i)
    return list_of_file_to_upload


def save_dict_into_json(path_json: str, content: dict):
    """Save text into new line a a text file. Creates the text file if needed

    Parameters
    ----------
    path_text_file : str
        path of the text file
    line : str
        text to add as new line
    """

    # create folder if not exists
    if not os.path.exists(os.path.dirname(path_json)):
        os.makedirs(os.path.dirname(path_json))

    # load the current JSON content
    if os.path.exists(path_json):
        with open(path_json, "r") as jsonFile:
            list_content = json.load(jsonFile)
    else:
        list_content = []

    # Add new content
    list_content.append(content)

    # Save the JSON
    with open(path_json, "w") as jsonFile:
        json.dump(list_content, jsonFile, indent=4)


def remove_file_in_folder(raw_folder_path: str, file_name: str) -> None:
    """Remove file on folder and subfolder ased on its name

    Parameters
    ----------
    raw_folder_path : str
        Parent folder path
    file_name : str
        Name of the file to remove
    """

    list_of_path = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(raw_folder_path)
        for f in filenames
        if f == file_name
    ]

    for i in list_of_path:
        os.remove(i)


def upload_to_zenodo(
    folder_path_in: str,
    folder_path_out_raw: str,
    depo_id: str,
    access_token=str,
    create_url_txt_file: bool = True,
    remove_file=False,
):

    # Remove existing URLs text file
    url_text_file_name = "url.json"
    list_of_elements_in_path = os.path.normpath(folder_path_in).split(os.sep)
    index_raw_folder = list_of_elements_in_path.index("Raw")
    rest_of_path = list_of_elements_in_path[index_raw_folder + 1 :]
    path_folder_to_remove_urls_json = os.path.join(folder_path_out_raw, *rest_of_path)
    remove_file_in_folder(path_folder_to_remove_urls_json, url_text_file_name)

    # List of file paths to upload
    list_path_to_upload = get_list_file_paths_to_load_to_zenodo(folder_path_in)

    # Upload
    for file_path in list_path_to_upload:
        time.sleep(2)

        list_of_elements_in_path = os.path.normpath(file_path).split(os.sep)
        index_raw_folder = list_of_elements_in_path.index("Raw")
        data_source_name = list_of_elements_in_path[index_raw_folder + 1]
        campaign_name = list_of_elements_in_path[index_raw_folder + 2]
        station_name = list_of_elements_in_path[index_raw_folder + 4]
        rest_of_path = list_of_elements_in_path[index_raw_folder + 5 :]

        # Connect to zenodo
        zen_files = pynodo.DepositionFiles(
            deposition=depo_id, access_token=access_token, sandbox=False
        )

        # Load data to zenodo
        filename = os.path.basename(file_path)
        filename_zenodo = str(uuid.uuid4().hex)
        t_init = datetime.now()
        zen_files.upload(file_path, filename_zenodo)
        duration = datetime.now() - t_init
        logging.info(f"{file_path} has been uploaded in {duration.total_seconds()} sec")

        # Get zenodo metadata
        list_of_file = zen_files.list()
        temp_dict = {}
        temp_dict["file_name"] = filename
        # temp_dict['filename_zenodo'] = filename_zenodo
        # temp_dict['repository_id='] = DEPO_ID
        # temp_dict['campaign_name='] = campaign_name
        # temp_dict['station_name='] = station_name
        # temp_dict['file_path='] = rest_of_path

        if list_of_file.get(filename_zenodo, None):
            # temp_dict['filesize'] = list_of_file.get(filename_zenodo).filesize
            # temp_dict['id'] = list_of_file.get(filename_zenodo).id
            # temp_dict['url'] = list_of_file.get(filename_zenodo).download
            temp_dict[
                "url"
            ] = f"https://zenodo.org/record/{DEPO_ID}/files/{filename_zenodo}"
            file_path_json = os.path.join(
                path_folder_out_raw,
                data_source_name,
                campaign_name,
                "data",
                station_name,
                url_text_file_name,
            )

            # if remove_file :
            #     os.remove(file_path)

            # Create URLs text file
            if create_url_txt_file:
                save_dict_into_json(file_path_json, temp_dict)

        else:
            logging.error(f"Error while upload file {filename}")


upload_to_zenodo(
    path_folder_in,
    path_folder_out_raw,
    depo_id=DEPO_ID,
    access_token=ACCESS_TOKEN,
    create_url_txt_file=True,
    remove_file=False,
)
