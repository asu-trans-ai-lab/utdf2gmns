# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, August 26th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import pandas as pd
import math


df_node = pd.read_csv("nodes.csv")
xy_list = df_node[['X', 'Y']].values.tolist()


def calculate_new_coordinates_from_offsets(initial_latitude, initial_longitude, x_offset_ft, y_offset_ft):

    EARTH_RADIUS = 6371.0088  # in kilometers

    # covert ft to km, 1 ft = 0.3048 m = 0.0003048 km
    x_distance_km = x_offset_ft * 0.0003048
    y_distance_km = y_offset_ft * 0.0003048

    # covert lat and lng degree to km
    lat_rad = math.radians(initial_latitude)
    lat_km_per_degree = (2 * math.pi * EARTH_RADIUS) * math.cos(lat_rad) / 360
    lng_km_per_degree = (2 * math.pi * EARTH_RADIUS) * math.cos(math.radians(initial_latitude)) / 360

    # calculate the lat and lng degree change with distance
    lat_change = y_distance_km / lat_km_per_degree
    lng_change = x_distance_km / lng_km_per_degree

    # calculate the new lat and lng
    new_lat = initial_latitude + lat_change
    new_lng = initial_longitude + lng_change

    return new_lat, new_lng


# Initial coordinates
initial_lat = 40.7128  # Example latitude
initial_lon = -74.0060  # Example longitude

# Distances in kilometers
x_distance_ft = 1000
y_distance_ft = 0

new_lat, new_lon = calculate_new_coordinates_from_offsets(
    initial_lat, initial_lon, x_distance_ft, y_distance_ft)

print("Initial Latitude:", initial_lat)
print("Initial Longitude:", initial_lon)
print("Updated Latitude:", new_lat)
print("Updated Longitude:", new_lon)





