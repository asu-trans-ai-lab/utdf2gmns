# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, January 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
import pickle
from pathlib import Path

import pandas as pd
from func_lib.geocoding_intersection import generate_coordinates_from_intersection
from func_lib.match_node_intersection_movement_utdf import (
    match_intersection_node, match_movement_and_intersection_node,
    match_movement_utdf_lane, match_movement_utdf_phase_timeplans)
from func_lib.read_utdf import (generate_intersection_data_from_utdf,
                                read_UTDF_file)
from utils_lib.package_settings import required_files, required_files_sub
from utils_lib.utility_lib import (check_required_files_exist,
                                   func_running_time,
                                   get_file_names_from_folder_by_type,
                                   path2linux, validate_filename)
pd.options.mode.chained_assignment = None  # default='warn'


@func_running_time
def generate_utdf_dict_of_dataframes(utdf_filename: str, city_name: str) ->dict:
    # read single UTDF file and produce data conversion and store data into a dictionary

    # read UTDF file and create dataframes of utdf_geo and utdf_lane
    utdf_dict_data = read_UTDF_file(utdf_filename)
    df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data, city_name)

    # geocoding utdf_intersection
    df_utdf_geo = generate_coordinates_from_intersection(df_utdf_intersection)

    # store utdf_geo and utdf_lane into utdf_dict_data
    utdf_dict_data["utdf_geo"] = df_utdf_geo

    # store object into pickle file
    # with open(os.path.join(os.getcwd(), "utdf2gmns.pickle"), 'wb') as f:
    #     pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)

    return utdf_dict_data


@func_running_time
def generate_movement_utdf(input_dir: list, city_name: list, isSave2csv: bool = True) -> list[pd.DataFrame]:

    # check if required files exist in the input directory
    files_from_directory = get_file_names_from_folder_by_type(input_dir, file_type="csv")

    # if not required, raise an exception
    isRequired = check_required_files_exist(required_files, files_from_directory)
    isRequired_sub = check_required_files_exist(required_files_sub, files_from_directory)

    # required fils are not found, raise an exception
    if not isRequired:
        raise Exception(f"Required files {required_files} are not found!")

    # read UTDF file and create dataframes of utdf_intersection and utdf_lane
    path_utdf = path2linux(os.path.join(input_dir, "UTDF.csv"))
    utdf_dict_data = generate_utdf_dict_of_dataframes(path_utdf, city_name)

    # required_sub files are not found, will return utdf_intersection and utdf_lane
    if not isRequired_sub:
        print("Because node.csv and movement.csv are not found, the function will return data from utdf in a dictionary, keys are: Lanes, Nodes, Networks, Timeplans, Links and utdf_geo.\n")

        # store object into pickle file
        with open(path2linux(os.path.join(os.getcwd(),"utdf2gmns.pickle")), 'wb') as f:
            pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)
        return utdf_dict_data

    # get the path of each file, since the input directory and files are checked, no need to validate the filename
    path_node = path2linux(os.path.join(input_dir, "node.csv"))
    path_movement = path2linux(os.path.join(input_dir, "movement.csv"))

    # read node and movement files
    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)

    # match utdf_intersection_geo with node
    print("Performing data matching between df_utdf_intersection_geo and node...")
    df_intersection_node = match_intersection_node(utdf_dict_data.get("utdf_geo"), df_node)

    # match movement with intersection_node
    print("Performing data matching between movement and intersection_node...")
    df_movement_intersection = match_movement_and_intersection_node(df_movement, df_intersection_node)

    # match movement with utdf_lane
    print("Performing data matching between movement_geo and utdf_lane...")
    df_movement_utdf_lane = match_movement_utdf_lane(
        df_movement_intersection, utdf_dict_data)

    # match movement with utdf_lane
    print("Performing data matching between movement_utdf_lane and utdf_phase_timeplans...")
    df_movement_utdf_phase = match_movement_utdf_phase_timeplans(
        df_movement_utdf_lane, utdf_dict_data)

    # store utdf_intersection_geo and movement_utdf in utdf_dict_data and return udf_intersection_nodetdf_dict_data
    utdf_dict_data["movement_utdf_phase"] = df_movement_utdf_phase
    utdf_dict_data["utdf_geo_GMNS_node"] = df_intersection_node

    # save the output file, the default isSave2csv is True
    # the output path is user's current working directory, output file name is movement_utdf.csv
    if isSave2csv:
        output_file_name = validate_filename(os.path.join(os.getcwd(),"movement_utdf.csv"))
        df_movement_utdf_phase.to_csv(output_file_name, index=False)

        output_file_name = validate_filename(os.path.join(os.getcwd(),"utdf_intersection.csv"))
        df_intersection_node.to_csv(output_file_name, index=False)

        with open(path2linux(os.path.join(os.getcwd(), "utdf2gmns.pickle")), 'wb') as f:
            pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)

    return [df_movement_utdf_phase, utdf_dict_data]


if __name__ == '__main__':

    dir_current = Path(__file__).parent
    input_dir = path2linux(os.path.join(dir_current.parent, "datasets", "data_ASU_network_2"))

    path_utdf = path2linux(os.path.join(input_dir, "UTDF.csv"))

    city_name = " Tempe, AZ"

    # utdf_dict_data = generate_utdf_dict_of_dataframes(path_utdf, city_name)

    df_movement_utdf_phase, utdf_dict_data = generate_movement_utdf(input_dir, city_name, isSave2csv=False)
