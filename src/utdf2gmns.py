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
from package_settings import required_files, required_files_sub
import os
import pickle


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

    # check if required files exist in the input directory
    files_from_directory = get_file_names_from_folder_by_type(
        input_dir, file_type="csv")

    # if not required, raise an exception
    isRequired = check_required_files_exist(required_files, files_from_directory)
    isRequired_sub = check_required_files_exist(required_files_sub, files_from_directory)

    # required fils are not found, raise an exception
    if not isRequired:
        raise Exception("Required files are not found!")

    # read UTDF file and create dataframes of utdf_intersection and utdf_lane
    path_utdf = os.path.join(input_dir, "UTDF.csv")
    utdf_dict_data = read_UTDF_file(path_utdf)
    df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data)
    df_utdf_lane = generate_lane_data_from_utdf(utdf_dict_data)

    # geocoding utdf_intersection to get utdf_intersection_geo
    df_utdf_intersection_geo = generate_coordinates_from_intersection(df_utdf_intersection)

    # required_sub files are not found, will return utdf_intersection and utdf_lane
    if not isRequired_sub:
        print("Because node.csv and movement.csv are not found, the function will return data from utdf in a dictionary, keys are: Lanes, Nodes, Networks, Timeplans, Links and utdf_intersection_geo.\n")

        # store utdf_intersection_geo into utdf_dict_data and return utdf_dict_data
        utdf_dict_data["utdf_intersection_geo"] = df_utdf_intersection_geo

        # store object into pickle file
        with open(os.path.join(os.getcwd(),"utdf2gmns.pickle"), 'wb') as f:
            pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)
        return utdf_dict_data

    # get the path of each file, since the input directory and files are checked, no need to validate the filename
    path_node = os.path.join(input_dir, "node.csv")
    path_movement = os.path.join(input_dir, "movement.csv")

    # read node and movement files
    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)

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

        output_file_name = validate_filename(os.path.join(os.getcwd(),"intersection_utdf.csv"))
        df_intersection_node.to_csv(output_file_name, index=False)

        # store utdf_intersection_geo and movement_utdf in utdf_dict_data and return udf_intersection_nodetdf_dict_data
        utdf_dict_data["utdf_intersection_geo"] = df_utdf_intersection_geo
        utdf_dict_data["movement_utdf"] = df_movement_utdf
        with open(os.path.join(os.getcwd(),"utdf2gmns.pickle"), 'wb') as f:
            pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)

    return [df_movement_utdf, df_intersection_node]


if __name__ == '__main__':

    # utdf to utdf_geo and utdf_lane
    # utdf2geolane
    # geolane2movement_utdf

    path_input_dir = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1"
    path_input_dir = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_tempe"


    df_movement_utdf = generate_movement_utdf(path_input_dir)
