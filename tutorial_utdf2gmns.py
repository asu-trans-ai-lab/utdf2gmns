# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, June 23rd 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
import utdf2gmns as ug
import pandas as pd

if __name__ == "__main__":

    city = " Bullhead City, AZ"
    path = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_bullhead_seg4"

    # get user added intersection data
    path_user_added_intersection = fr"{path}\utdf_intersection_sample.csv"

    # option= 1, generate movement_utdf.csv directly
    # option= 2, generate movement_utdf.csv step by step (more flexible)
    option = 3

    if option == 1:
        # NOTE: Option 1, generate movement_utdf.csv directly

        res = ug.generate_movement_utdf(path, city, isSave2csv=False,
                                        path_utdf_intersection=path_user_added_intersection)

    if option == 2:
        # NOTE: Option 2, generate movement_utdf.csv step by step (more flexible)
        path_utdf = fr"{path}\UTDF.csv"
        path_node = fr"{path}\node.csv"
        path_movement = fr"{path}\movement.csv"

        # Step 1: read UTDF.csv
        utdf_dict_data = ug.generate_utdf_dataframes(path_utdf, city)

        # Step 1.1: get intersection data from UTDF.csv
        df_intersection = utdf_dict_data["utdf_intersection"]

        # Step 1.2: geocoding intersection data

        # # Step 1.2.1: if user added intersection data, read it
        # df_intersection_geo = pd.read_csv(path_user_added_intersection)

        # Step 1.2.2: else generate intersection data from UTDF.csv
        df_intersection_geo = ug.generate_coordinates_from_intersection(df_intersection)

        # Step 2: read node.csv and movement.csv
        df_node = pd.read_csv(path_node)
        df_movement = pd.read_csv(path_movement)

        # Step 3: match intersection_geo and node
        df_intersection_node = ug.match_intersection_node(df_intersection_geo, df_node, max_distance_threshold=0.1)

        # Step 4: match movement and intersection_node
        df_movement_intersection = ug.match_movement_and_intersection_node(df_movement, df_intersection_node)

        # Step 5: match movement and utdf_lane
        df_movement_utdf_lane = ug.match_movement_utdf_lane(df_movement_intersection, utdf_dict_data)

        # Step 6: match movement and utdf_phase_timeplans
        df_movement_utdf_phase = ug.match_movement_utdf_phase_timeplans(df_movement_utdf_lane, utdf_dict_data)

        # Step 7: sve movement_utdf.csv
        df_movement_utdf_phase.to_csv(fr"{path}\movement_utdf.csv", index=False)

#     path_utdf = fr"{path}\UTDF.csv"
#     utdf_dict_data = ug.generate_utdf_dataframes(path_utdf, city)
#
#     df_lane_formated = ug.reformat_lane_dataframe(utdf_dict_data)
#
