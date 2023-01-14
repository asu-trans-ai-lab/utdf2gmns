# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, November 28th 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from geopy.geocoders import Nominatim
import pandas as pd
import geocoder
import googlemaps
import math


def calculate_distance_from_two_points(point1: tuple, point2: tuple) -> float:

    lat1, lon1 = point1
    lat2, lon2 = point2
    radius = 6371  # radius of earth in km

    lat_diff = math.radians(lat2-lat1)
    lon_diff = math.radians(lon2-lon1)
    a = math.sin(lat_diff/2) * math.sin(lat_diff / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(lon_diff / 2) * math.sin(lon_diff / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c  # distance in km

    return distance


def googlemaps_geocoding_from_address(address, api_key) -> tuple:

    # initialize googlemaps client
    gmaps = googlemaps.Client(key=api_key)

    # Geocoding an address
    location_instance = gmaps.geocode(address)

    # get the location
    location_lng_lat = (location_instance[0]['geometry']['location']['lat'], location_instance[0]['geometry']['location']['lng'])

    return location_lng_lat


def geopy_geocoding_from_address(address: str) -> tuple:

    # initialize geopy client
    geo_locator = Nominatim(user_agent="myGeopyGeocoder")

    # Geocoding an address
    try:
        location = geo_locator.geocode(address, timeout=10)
        location_lng_lat = (location.longitude, location.latitude)
    except Exception as e:

        location_lng_lat = (0,0)
        print(
            f"Error: {address} is not able to geocode, for {e}, try to use (0 ,0) to as lng and lat \n")

    return location_lng_lat


def geocoder_geocoding_from_address(address: str) -> tuple:

    # initialize geocoder arcgis client
    location_instance = geocoder.arcgis(address).geojson

    # get the location
    location_lng_lat = (location_instance["features"][0]["geometry"]["coordinates"])

    return location_lng_lat


def generate_coordinates_from_csv(path_input: str, distance_threshold = 0.01) -> pd.DataFrame:
    # distance_threshold is the threshold to determine whether the intersection is able to geocode, using km as unit

    # TDD development
    if not isinstance(path_input, str):
        raise Exception("path_input should be a string.")

    # Step 2: read data
    df = pd.read_csv(path_input)

    # Step 3: generate full address values from columns intersection_name and city_name

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
    intersection_full_name_list = df["full_name_intersection"].tolist()
    intersection_full_name_reversed_list = df["full_name_intersection_reversed"].tolist()

    lnglat_values_full_name = [geocoder_geocoding_from_address(address) for address in intersection_full_name_list]
    lnglat_values_full_name_reversed = [geocoder_geocoding_from_address(address) for address in intersection_full_name_reversed_list]

    # create new column named distance_from_full_name
    distance = [calculate_distance_from_two_points(lnglat_values_full_name[i], lnglat_values_full_name_reversed[i]) for i in range(len(lnglat_values_full_name))]

    for i in range(len(df)):
        df["distance_from_full_name"] = distance

        if distance[i] <= distance_threshold:
            df.loc[i, "x_coord"] = lnglat_values_full_name[i][0]
            df.loc[i, "y_coord"] = lnglat_values_full_name[i][1]

        else:
            # use None to indicate the intersection is not able to geocode
            df.loc[i, "x_coord"] = None
            df.loc[i, "y_coord"] = None

    created_column_names = ["reversed_intersection_name", "full_name_intersection", "full_name_intersection_reversed", "distance_from_full_name"]
    df_final = df.loc[:,~df.columns.isin(created_column_names)]

    return df_final

if __name__ == "__main__":

    # Step 1: input data path
    path_input = "intersection_from_synchro.csv"

    # Step 2: generate coordinates
    df = generate_coordinates_from_csv(path_input)

    # save to csv file
    df.to_csv("intersection_from_synchro_with_coordinates.csv", index=False)
