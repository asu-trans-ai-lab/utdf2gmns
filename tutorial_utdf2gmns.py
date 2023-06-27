# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, June 23rd 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import utdf2gmns as ug
import pandas as pd

if __name__ == "__main__":

    city = " Bullhead City, AZ"

    # option= 1, generate movement_utdf.csv directly
    # option= 2, generate movement_utdf.csv step by step (more flexible)
    option = 2

    if option == 1:
        # NOTE: Option 1, generate movement_utdf.csv directly
        path = r"C:\Users\roche\Desktop\coding\data_bullhead_seg4"

        res = ug.generate_movement_utdf(path, city, isSave2csv=True)

    if option == 2:
        # NOTE: Option 2, generate movement_utdf.csv step by step (more flexible)
        path_utdf = r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\UTDF.csv"
        path_node = r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\node.csv"
        path_movement = r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\movement.csv"

        # Step 1: read UTDF.csv
        utdf_dict_data = ug.generate_utdf_dataframes(path_utdf, city)

        # Step 1.1: get intersection data from UTDF.csv
        df_intersection = utdf_dict_data["utdf_intersection"]

        # Step 1.2: geocoding intersection data
        df_intersection_geo = ug.generate_coordinates_from_intersection(df_intersection)

        # Step 2: read node.csv and movement.csv
        df_node = pd.read_csv(path_node)
        df_movement = pd.read_csv(path_movement)

        # Step 3: match intersection_geo and node
        df_intersection_node = ug.match_intersection_node(df_intersection_geo, df_node)

        # Step 4: match movement and intersection_node
        df_movement_intersection = ug.match_movement_and_intersection_node(df_movement, df_intersection_node)

        # Step 5: match movement and utdf_lane
        df_movement_utdf_lane = ug.match_movement_utdf_lane(df_movement_intersection, utdf_dict_data)

        # Step 6: match movement and utdf_phase_timeplans
        df_movement_utdf_phase = ug.match_movement_utdf_phase_timeplans(df_movement_utdf_lane, utdf_dict_data)
