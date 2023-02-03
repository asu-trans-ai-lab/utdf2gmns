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
from utils_lib.utility_lib import (func_running_time,
                         get_file_names_from_folder_by_type,
                         check_required_files_exist,
                         validate_filename)
# from package_settings import required_files, required_files_sub
import os
import pickle


@func_running_time
def generate_utdf_geo_lane(utdf_filename: str, city_name: str, isAllCategories: bool = False) ->dict:
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

    if not isAllCategories:
        # return a dictionary with only utdf_geo and utdf_lane
        return {"utdf_geo": utdf_dict_data.get("utdf_geo"), "utdf_lane": utdf_dict_data.get("utdf_lane")}
    return utdf_dict_data


@func_running_time
def perform_data_matching(matching_dict: dict) -> dict:
    # you need to prepare node, movement, utdf_geo, and utdf_lane dataframes first and store them into a dictionary
    # matching_dict: {"utdf_geo": utdf_geo, "utdf_lane": utdf_lane, "node": node, "movement": movement}

    df_node = matching_dict.get("node")
    df_utdf_geo = matching_dict.get("utdf_geo")
    df_movement = matching_dict.get("movement")
    df_utdf_lane = matching_dict.get("utdf_lane")

    # match utdf_geo with node
    print("Performing data matching between utdf_geo and node...")
    df_intersection_node = match_intersection_node(df_utdf_geo, df_node)

    # match movement with intersection_node
    print("Performing data matching between movement and intersection_node...")
    df_movement_geo = match_movement_and_intersection_node(df_movement, df_intersection_node)

    # match movement with utdf_lane
    print("Performing data matching between movement_geo and utdf_lane...")
    df_movement_utdf = match_movement_utdf(df_movement_geo, df_utdf_lane)

    matching_dict["movement_utdf"] = df_movement_utdf
    return matching_dict


@func_running_time
def generate_movement_utdf(input_filename_list: list, city_name_list: list,  node_movement_dir: str, isSave2csv: bool = True) -> pd.DataFrame:

    # define a empty dictionary to store all data
    utdf2gmns_dict = {}
    utdf_movement_dict = {}

    # Check node.csv and movement.csv exist in the current directory or not


    # # check if required files exist in the input directory
    # files_from_directory = get_file_names_from_folder_by_type(input_dir, file_type="csv")

    # # if not required, raise an exception
    # isRequired = check_required_files_exist(required_files, files_from_directory)
    # isRequired_sub = check_required_files_exist(required_files_sub, files_from_directory)

    # # required fils are not found, raise an exception
    # if not isRequired:
    #     raise Exception("Required files are not found!")

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


    city_name = " Tempe, AZ"

    # path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_ASU_network\UTDF.csv"
    # path_node = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_ASU_network\node.csv"
    # path_movement = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_ASU_network\movement.csv"

    path_utdf = r"../datasets/data_bullhead_city_network/UTDF.csv"
    path_node = r"../datasets/data_bullhead_city_network/node.csv"
    path_movement = r"../datasets/data_bullhead_city_network/movement.csv"

    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)

    utdf_dict_data = generate_utdf_geo_lane(path_utdf, city_name)
    matching_dict = {**utdf_dict_data, **{"node": df_node, "movement": df_movement}}
    utdf2gmns_dict = perform_data_matching(matching_dict)
    movement_utdf = utdf2gmns_dict.get("movement_utdf")
    utdf_geo = utdf2gmns_dict.get("utdf_geo")

    movement_utdf.to_csv("movement_utdf.csv", index=False)
    utdf_geo.to_csv("utdf_geo.csv", index=False)


    # utdf_dict_data = read_UTDF_file(path_utdf)
    # df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data, city_name)
    # # geocoding utdf_intersection
    # df_utdf_geo = generate_coordinates_from_intersection(df_utdf_intersection)
    # # store utdf_geo and utdf_lane into utdf_dict_data
    # utdf_dict_data["utdf_geo"] = df_utdf_geo
    # matching_dict = {**utdf_dict_data, **{"node": df_node, "movement": df_movement}}
    # utdf2gmns_dict = perform_data_matching(matching_dict)
    # movement_utdf = utdf2gmns_dict.get("movement_utdf")
    # utdf_geo = utdf2gmns_dict.get("utdf_geo")

    # df_movement_utdf = generate_movement_utdf(path_input_dir)
