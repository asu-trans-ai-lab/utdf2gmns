# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, December 3rd 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import pandas as pd
from utdf2gmns.utils_lib.utility_lib import func_running_time, calculate_point2point_distance_in_km


def find_shortest_distance_node(point: tuple,
                                node_df: pd.DataFrame,
                                max_distance_threshold: float = 0.1,
                                intersection_id="") -> tuple:
    """ point: a tuple of (longitude, latitude),
        node_df: a dataframe of node information,
        max_distance_threshold (km): the maximum distance threshold to find the nearest node
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
        print(f"  :Intersection id: {intersection_id} can not find the nearest node within threshold of {max_distance_threshold}km")
        return [""] * len(node_df.columns)

    # find the index of the minimum distance
    min_distance_index = point_to_node_distance_list.index(min_distance)
    return list(node_df.loc[min_distance_index, :])


@func_running_time
def match_intersection_node(df_intersection_geo: pd.DataFrame,
                            df_node: pd.DataFrame,
                            max_distance_threshold=0.1) -> pd.DataFrame:

    # get valid node data with ctrl_type = signal
    df_node_signal = df_node[df_node["ctrl_type"] == "signal"].reset_index(drop=True)

    # mach intersection_geo with node
    col_intersection_geo = list(df_intersection_geo.columns)
    col_node = list(df_node_signal.columns)

    intersection_node_list = []
    for i in range(len(df_intersection_geo)):

        intersection_value = list(df_intersection_geo.loc[i, :])

        intersection_lnglat = (
            df_intersection_geo.loc[i, "coord_x"], df_intersection_geo.loc[i, "coord_y"])

        inter_id = df_intersection_geo.loc[i, "intersection_id"]

        intersection_node_list.append(
            intersection_value + find_shortest_distance_node(intersection_lnglat,
                                                             df_node_signal,
                                                             max_distance_threshold,
                                                             intersection_id=inter_id))

    df_intersection_node = pd.DataFrame(
        intersection_node_list, columns=col_intersection_geo + col_node)

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

        # filter the intersection_node by osm_node_id
        matched_intersection_node_list = list(
            df_intersection_node[df_intersection_node["osm_node_id"] == movement_osm_node_id].values)

        # filtered intersection node value
        matched_intersection_node = list(
            matched_intersection_node_list[0]) if matched_intersection_node_list else [""] * len(col_intersection_node)

        # append data to movement_intersection_list
        movement_intersection_list.append(
            list(df_movement.loc[k, :]) + matched_intersection_node)

    df_movement_intersection = pd.DataFrame(
        movement_intersection_list,
        columns=col_movement + col_intersection_node)

    return df_movement_intersection


@func_running_time
def match_movement_utdf_lane(df_movement_intersection: pd.DataFrame, utdf_dict_data: dict) -> pd.DataFrame:
    # Add Synchro/utdf data to movement_intersection_node
    df_utdf_lanes = utdf_dict_data.get("Lanes")
    print(f"  : There are {df_utdf_lanes.shape[0]} utdf lanes")

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

    df_movement_utdf_lane = pd.concat(movement_utdf_list, sort=False)

    return df_movement_utdf_lane

@func_running_time
def match_movement_utdf_phase_timeplans(df_movement_utdf_lane: pd.DataFrame, utdf_dict_data: dict) -> pd.DataFrame:

    df_utdf_phase_timeplans = utdf_dict_data.get("phase_timeplans")

    df_movement_utdf_lane["synchro_INTID"] = df_movement_utdf_lane["synchro_INTID"].astype(str)
    df_utdf_phase_timeplans["INTID"] = df_utdf_phase_timeplans["INTID"].astype(str)

    return pd.merge(df_movement_utdf_lane, df_utdf_phase_timeplans, left_on="synchro_INTID", right_on="INTID", how="left")
