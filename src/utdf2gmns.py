# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, January 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import pandas as pd
from func_lib.read_utdf import (read_UTDF_file,
                                generate_intersection_data_from_utdf,
                                generate_lane_data_from_utdf)
from func_lib.geocoding_intersection import generate_coordinates_from_intersection
from func_lib.match_node_intersection_movement_utdf import (match_intersection_node,
                                                            match_movement_and_intersection_node,
                                                            match_movement_utdf)
from utility_lib import (func_running_time,
                         get_file_names_from_folder_by_type,
                         check_required_files_exist,
                         validate_filename)
from package_settings import required_files
import os


@func_running_time
def generate_movement_utdf(input_dir: str, isSave2csv: bool = True) -> pd.DataFrame:
    """Main function to generate movement_utdf.csv

    Args:
        input_dir (str): the directory that contains UTDF.csv, node.csv, and movement.csv
        isSave2csv (bool, optional): save matched file to csv. Defaults to True.

    Raises:
        Exception: Required files are not found in the given directory!

    Returns:
        pd.DataFrame: the dataframe of movement_utdf
    """

    # check if the required files exist in the input directory
    files_from_directory = get_file_names_from_folder_by_type(
        input_dir, file_type="csv")

    # if not required, raise an exception
    isRequired = check_required_files_exist(required_files, files_from_directory)
    if not isRequired:
        raise Exception("Required files are not found!")

    # get the path of each file, since the input directory and files are checked, no need to validate the filename
    path_utdf = os.path.join(input_dir, "UTDF.csv")
    path_node = os.path.join(input_dir, "node.csv")
    path_movement = os.path.join(input_dir, "movement.csv")

    # read utdf file and create dataframes of utdf_intersection and utdf_lane
    utdf_dict_data = read_UTDF_file(path_utdf)
    df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data)
    df_utdf_lane = generate_lane_data_from_utdf(utdf_dict_data)

    # read node and movement files
    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)

    # geocoding utdf_intersection to get utdf_intersection_geo
    df_utdf_intersection_geo = generate_coordinates_from_intersection(df_utdf_intersection)

    # match utdf_intersection_geo with node
    df_intersection_node = match_intersection_node(df_utdf_intersection_geo, df_node)

    # match movement with intersection_node
    df_movement_intersection = match_movement_and_intersection_node(df_movement, df_intersection_node)

    # match movement with utdf_lane
    df_movement_utdf = match_movement_utdf(df_movement_intersection, df_utdf_lane)

    # save the output file, the default isSave2csv is True
    # the output path is user's current working directory, output file name is movement_utdf.csv
    if isSave2csv:
        output_file_name = validate_filename(os.path.join(os.getcwd(),"movement_utdf.csv"))
        df_movement_utdf.to_csv(output_file_name, index=False)

    return df_movement_utdf


if __name__ == '__main__':

    path_input_dir = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1"

    df_movement_utdf = generate_movement_utdf(path_input_dir)
