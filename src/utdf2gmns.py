# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, January 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import pandas as pd
from utdf_reading import read_UTDF_file, generate_intersection_data_from_utdf, generate_lane_data_from_utdf
from geocoding_intersection import generate_coordinates_from_intersection
from utdf_movement_data_merging import (match_intersection_node, match_movement_and_intersection_node, match_movement_utdf)
from utility_lib import (func_running_time,
                         get_file_names_from_folder_by_type,
                         check_required_files_exist,
                         validate_filename)
from proj_config import required_files
import os

def generate_movement_utdf(input_dir: str, isSave2csv: bool = True) -> pd.DataFrame:

    # check if the required files exist
    files_from_directory = get_file_names_from_folder_by_type(
        input_dir, file_type="csv")

    isRequired = check_required_files_exist(required_files, files_from_directory)
    if not isRequired:
        raise Exception("Required files are not found!")

    # read files
    path_utdf = os.path.join(input_dir, "UTDF.csv")
    path_node = os.path.join(input_dir, "node.csv")
    path_movement = os.path.join(input_dir, "movement.csv")

    utdf_dict_data = read_UTDF_file(path_utdf)
    df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data)
    df_utdf_lane = generate_lane_data_from_utdf(utdf_dict_data)
    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)

    # geocoding intersection data
    df_utdf_intersection_geo = generate_coordinates_from_intersection(df_utdf_intersection)

    # match intersection_geo with node
    df_intersection_node = match_intersection_node(df_utdf_intersection_geo, df_node)

    # match movement with intersection_node
    df_movement_intersection = match_movement_and_intersection_node(df_movement, df_intersection_node)
    # df_movement_intersection.to_csv("movement_intersection.csv", index=False)

    # match movement with synchro
    df_movement_utdf = match_movement_utdf(df_movement_intersection, df_utdf_lane)

    if isSave2csv:
        output_file_name = validate_filename(os.path.join(os.getcwd(),"movement_utdf.csv"))
        df_movement_utdf.to_csv(output_file_name, index=False)

    return df_movement_utdf
    # return df_movement_intersection, df_utdf_lane


if __name__ == '__main__':

    path_input_dir = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1"

    df_movement_utdf = generate_movement_utdf(path_input_dir)

