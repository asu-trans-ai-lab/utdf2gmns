# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, November 28th 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# from geopy.geocoders import Nominatim
# import googlemaps
import contextlib
# import os
# import sys
from multiprocessing import Pool
# from pathlib import Path

import geocoder
import pandas as pd

from utdf2gmns.utils_lib.utility_lib import (
    calculate_point2point_distance_in_km, func_running_time)

# def googlemaps_geocoding_from_address(address, api_key) -> tuple:
#
#     # initialize googlemaps client
#     gmaps = googlemaps.Client(key=api_key)
#
#     # Geocoding an address
#     location_instance = gmaps.geocode(address)
#
#     # get the location
#     location_lng_lat = (location_instance[0]['geometry']['location']['lat'], location_instance[0]['geometry']['location']['lng'])
#
#     return location_lng_lat
#
#
# def geopy_geocoding_from_address(address: str) -> tuple:
#
#     # initialize geopy client
#     geo_locator = Nominatim(user_agent="myGeopyGeocoder")
#
#     # Geocoding an address
#     try:
#         location = geo_locator.geocode(address, timeout=10)
#         location_lng_lat = (location.longitude, location.latitude)
#     except Exception as e:
#
#         location_lng_lat = (0,0)
#         print(
#             f"Error: {address} is not able to geocode, for {e}, try to use (0 ,0) to as lng and lat \n")
#
#     return location_lng_lat


def geocoder_geocoding_from_address(address: str) -> tuple:

    # initialize geocoder arcgis client
    location_instance = geocoder.arcgis(address).geojson

    # get the location
    try:
        location_lng_lat = (
            location_instance["features"][0]["geometry"]["coordinates"])
    except Exception:
        location_lng_lat = [0, 0]

    return location_lng_lat


@func_running_time
def generate_coordinates_from_intersection(df_intersection: pd.DataFrame, distance_threshold=0.01) -> pd.DataFrame:
    # distance_threshold is the threshold to determine whether the intersection is able to geocode, using km as unit

    df = df_intersection.copy()

    # check required columns exist in the dataframe
    if not {"intersection_name", "city_name"}.issubset(set(df.columns)):
        raise Exception(
            "intersection_name and city_name are not in the dataframe, please check the input file.")

    # Create one column named "reversed_intersection_name"
    for i in range(len(df)):
        if "&" in df.loc[i, "intersection_name"]:
            df.loc[i, "reversed_intersection_name"] = df.loc[i, "intersection_name"].split(
                "&")[1] + " & " + df.loc[i, "intersection_name"].split(" & ")[0]
        else:
            df.loc[i, "reversed_intersection_name"] = df.loc[i, "intersection_name"]

    # create two columns named "full_name_intersection" and "full_name_intersection_reversed"
    df["full_name_intersection"] = df["intersection_name"] + ", " + df["city_name"]
    df["full_name_intersection_reversed"] = df["reversed_intersection_name"] + ", " + df["city_name"]

    # Step 4: geocoding
    print("   :geocoding intersections...")
    intersection_full_name_list = df["full_name_intersection"].tolist()
    intersection_full_name_reversed_list = df["full_name_intersection_reversed"].tolist()

    # the number of intersections to be geocoded
    num_intersection = len(intersection_full_name_list)

    try:
        lnglat_values_full_name = []
        lnglat_values_full_name_reversed = []
        for i in range(num_intersection):
            lnglat_values_full_name.append(
                geocoder_geocoding_from_address(intersection_full_name_list[i]))
            lnglat_values_full_name_reversed.append(
                geocoder_geocoding_from_address(intersection_full_name_reversed_list[i]))

            if i % 10 == 0:
                print(f"    :{i}/{num_intersection} intersections have been geocoded.")

        # use multiprocessing to speed up
        # p = Pool()
        # lnglat_values_full_name = p.map(geocoder_geocoding_from_address, intersection_full_name_list)

        # p1 = Pool()
        # lnglat_values_full_name_reversed = p1.map(geocoder_geocoding_from_address, intersection_full_name_reversed_list)

    except Exception as e:
        raise Exception("   :geocoding intersections failed, try again...") from e


    # create new column named distance_from_full_name
    print("   :cross validating...")
    distance = [calculate_point2point_distance_in_km(
        lnglat_values_full_name[i], lnglat_values_full_name_reversed[i]) for i in range(len(lnglat_values_full_name))]

    for i in range(len(df)):
        df["distance_from_full_name"] = distance

        if distance[i] <= distance_threshold:
            df.loc[i, "coord_x"] = lnglat_values_full_name[i][0]
            df.loc[i, "coord_y"] = lnglat_values_full_name[i][1]

        else:
            # use None to indicate the intersection is not able to geocode
            df.loc[i, "coord_x"] = None
            df.loc[i, "coord_y"] = None

    created_column_names = ["reversed_intersection_name", "full_name_intersection",
                            "full_name_intersection_reversed", "distance_from_full_name"]
    df_final = df.loc[:, ~df.columns.isin(created_column_names)]

    # print summary information
    print(
        f" {len(df_final) - df_final['coord_x'].isna().sum()} / {len(df_final)} intersections geocoded.")
    print(
        f" {df_final['coord_x'].isna().sum()} / {len(df_final)} intersections are not able to geocode.")

    return df_final


if __name__ == "__main__":
    """
    We provided three geocoding methods: googlemaps, geopy and geocoder
    The example using geocoder and you don't need to install googlemaps and geopy as well(comment out the code if you want to use them)
    """

    # Step 1: input data path
    path_input = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1\utdf_intersection.csv"

    # Step 2: read data
    df_intersection = pd.read_csv(path_input)

    # Step 2: generate coordinates
    df = generate_coordinates_from_intersection(df_intersection)

    # save to csv file
    # df.to_csv(f"{path_input.split('.')[0]}_with_coordinates.csv", index=False)
