# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, December 3rd 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from typing import Union
import pandas as pd
from utility_lib import (func_running_time,
                         get_file_names_from_folder_by_type,
                         check_required_files_exist,
                         validate_filename)
from math import sin, cos, sqrt, atan2, radians, isnan
import os


def check_required_files(input_dir: Union[str, dict]) -> tuple:
    """ read required files and return a tuple of (node_df, movement_df) """

    # read files from directory
    if isinstance(input_dir, str) and os.path.isdir(input_dir):
        required_files = ["UTDF.csv", "node.csv", "movement.csv"]
    else:
        raise ValueError("The path_required_file should be a directory or a dictionary of file names")

    # check if the required files exist
    files_from_directory = get_file_names_from_folder_by_type(
        input_dir, file_type="csv")

    isRequired = check_required_files_exist(required_files, files_from_directory)
    # if isRequired:
    #     df_intersection = pd.read_csv(os.path.join(input_dir, "UTDF.csv"))
    #     df_node = pd.read_csv(os.path.join(input_dir, "node.csv"))
    #     df_movement = pd.read_csv(os.path.join(input_dir, "movement.csv"))

    # return (df_intersection, df_node, df_movement, df_utdf_lanes)
    return isRequired


def calculate_point2point_distance_in_km(point1: tuple, point2: tuple) -> float:
    """ point1 and point2: a tuple of (longitude, latitude) """

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1[1])
    lon1 = radians(point1[0])
    lat2 = radians(point2[1])
    lon2 = radians(point2[0])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # return math.pow((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2, 0.5)

    # the distance is in km
    return distance


def find_shortest_distance_node(point: tuple, node_df: pd.DataFrame, max_distance_threshold: float = 0.1) -> tuple:
    """ point: a tuple of (longitude, latitude),
        node_df: a dataframe of node information,
        max_distance_threshold: the maximum distance threshold to find the nearest node
    """

    # get node longitude and latitude from node_df
    node_location_list = [(node_df.loc[i, "x_coord"], node_df.loc[i, "y_coord"]) for i in range(node_df.shape[0])]

    # calculate the distance between point and each node
    point_to_node_distance_list = [calculate_point2point_distance_in_km(point, node_location) for node_location in node_location_list]

    # find the minimum distance
    min_distance = min(point_to_node_distance_list)
    # print(f"INFO: The minimum distance is {min_distance} km")

    # if the minimum distance is larger than the threshold, then return None
    if min_distance > max_distance_threshold:
        return []

    # find the index of the minimum distance
    min_distance_index = point_to_node_distance_list.index(min_distance)
    return list(node_df.loc[min_distance_index, :])


@func_running_time
def match_intersection_node(df_intersection_geo: pd.DataFrame, df_node: pd.DataFrame) -> pd.DataFrame:

    # get valid node data with ctrl_type = signal
    df_node_signal = df_node[df_node["ctrl_type"] == "signal"].reset_index(drop=True)

    #  mach intersection_geo with node
    col_intersection_geo = list(df_intersection_geo.columns)
    col_node = list(df_node_signal.columns)

    intersection_node_list = []
    for i in range(len(df_intersection_geo)):

        intersection_value = list(df_intersection_geo.loc[i, :])

        intersection_lnglat = (
            df_intersection_geo.loc[i, "coord_x"], df_intersection_geo.loc[i, "coord_y"])

        intersection_node_list.append(
            intersection_value + find_shortest_distance_node(intersection_lnglat, df_node_signal))

    df_intersection_node = pd.DataFrame(
        intersection_node_list, columns=col_intersection_geo + col_node)

    # df_intersection_node.to_csv("macro_intersection_node.csv", index=False)
    return df_intersection_node


@func_running_time
def match_movement_and_intersection_node(df_movement: pd.DataFrame, df_intersection_node: pd.DataFrame) -> pd.DataFrame:
    # match movement with intersection_node by osm_node_id
    col_movement = list(df_movement.columns)
    col_intersection_node = list(df_intersection_node.columns)

    movement_intersection_list = []
    for k in range(len(df_movement)):

        # get the osm_node_id of the movement
        movement_osm_node_id = df_movement.loc[k, "osm_node_id"]

        # get filter the intersection_node by osm_node_id
        matched_intersection_node_list = list(
            df_intersection_node[df_intersection_node["osm_node_id"] == movement_osm_node_id].values)

        # get filtered intersection node value
        matched_intersection_node = list(
            matched_intersection_node_list[0]) if matched_intersection_node_list else []

        # append data to movement_intersection_list
        movement_intersection_list.append(
            list(df_movement.loc[k, :]) + matched_intersection_node)

    df_movement_intersection = pd.DataFrame(
        movement_intersection_list,
        columns=col_movement + col_intersection_node)

    return df_movement_intersection


@func_running_time
def match_movement_utdf(df_movement_intersection: pd.DataFrame,
                        df_utdf_lanes: pd.DataFrame) -> pd.DataFrame:
    # Add Synchro/utdf data to movement_intersection_node

    intersection_id_list = [value for value in list(
        df_movement_intersection["synchro_INTID"].unique()) if value is not None]

    # get movement_intersection dataframe with and without id list
    df_with_id = df_movement_intersection[df_movement_intersection["synchro_INTID"].isin(
        intersection_id_list)]
    df_without_id = df_movement_intersection[~df_movement_intersection["synchro_INTID"].isin(
        intersection_id_list)]

    # get movement_intersection column name
    col_movement_intersection = list(df_movement_intersection.columns)

    # Add utdf info to df_with_id
    movement_utdf_list = [df_without_id]

    for intersection_id in intersection_id_list:
        # get movement_intersection_node dataframe by id
        df_with_id_single_id = df_with_id[
            df_with_id["synchro_INTID"] == intersection_id].reset_index(drop=True)

        # print(df_with_id_single_id)
        # get utdf_lane dataframe by id
        df_utdf_lanes_single_id = df_utdf_lanes[df_utdf_lanes["INTID"] == intersection_id].reset_index(drop=True)

        # print(df_synchro_single_id)
        df_utdf_lanes_single_id_dict = df_utdf_lanes_single_id.to_dict("list")
        col_synchro_added_info = df_utdf_lanes_single_id_dict.get(
            "RECORDNAME", [])

        union_list = []
        for j in range(len(df_with_id_single_id)):

            first_list = list(df_with_id_single_id.loc[j, :])

            movement_txt_id = df_with_id_single_id.loc[j, "mvmt_txt_id"]
            second_list = df_utdf_lanes_single_id_dict.get(movement_txt_id, [])

            union_list.append(first_list + second_list)

        movement_utdf_list.append(pd.DataFrame(
            union_list, columns=col_movement_intersection + col_synchro_added_info))

    # remove duplicated columns
    movement_utdf_list_removed_duplicated = [
        df.loc[:, ~df.columns.duplicated()] for df in movement_utdf_list]

    # get maximum column names from movement_synchro_list
    col_longest = sorted(movement_utdf_list_removed_duplicated,
                         key=lambda x: len(x.columns))[-1].columns

    # add missing columns to movement_synchro_list
    movement_utdf_list = [df.reindex(columns=col_longest, fill_value=None) for df in movement_utdf_list_removed_duplicated]

    df_movement_utdf = pd.concat(movement_utdf_list, sort=False)

    return df_movement_utdf


if __name__ == "__main__":

    # Prepare input path: can be either a dictionary or a directory string
    required_files_dict = {"UTDF": "./UTDF.csv",
                           "node": "./node.csv",
                           "movement": "./movement.csv"}

    path_input_directory = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1"

    # get input data
    file_dataframes = check_required_files(path_input_directory)

    df_intersection_geo = file_dataframes[0]
    df_node = file_dataframes[1]
    df_movement = file_dataframes[2]
    df_utdf_lanes = file_dataframes[3]

    # match intersection_geo with node
    df_intersection_node = match_intersection_node(df_intersection_geo, df_node)
    # df_intersection_node.to_csv("macro_intersection_node.csv", index=False)

    # match movement with intersection_node
    df_movement_intersection = match_movement_and_intersection_node(df_movement, df_intersection_node)
    # df_movement_intersection.to_csv("movement_intersection.csv", index=False)

    # match movement with synchro
    df_movement_synchro = match_movement_utdf(df_movement_intersection, df_utdf_lanes)
