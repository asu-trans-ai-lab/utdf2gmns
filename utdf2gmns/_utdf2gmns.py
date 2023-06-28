# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, January 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
import pickle

import pandas as pd

# For deployment
from utdf2gmns.func_lib.geocoding_intersection import \
    generate_coordinates_from_intersection
from utdf2gmns.func_lib.match_node_intersection_movement_utdf import (
    match_intersection_node, match_movement_and_intersection_node,
    match_movement_utdf_lane, match_movement_utdf_phase_timeplans)
from utdf2gmns.func_lib.read_utdf import (generate_intersection_data_from_utdf,
                                          read_UTDF_file)
from utdf2gmns.utils_lib.package_settings import (required_files,
                                                  required_files_sub,
                                                  utdf_city_name)
from utdf2gmns.utils_lib.utility_lib import (check_required_files_exist,
                                             func_running_time,
                                             get_filenames_from_folder_by_type,
                                             path2linux, validate_filename)

pd.options.mode.chained_assignment = None  # default='warn'


@func_running_time
def generate_utdf_dataframes(utdf_filename: str, city_name: str) -> dict:
    """read single UTDF file and produce data conversion and store data into a dictionary

    Parameters
    ----------
    utdf_filename : str
        the path of UTDF file
    city_name : str
        the name of the city where the UTDF file is located

    Returns
    -------
    dict
        a dictionary of utdf_dict_data including: Node, Link, Network, Lanes, Timeplans, Phases, utdf_intersection
    """

    # read UTDF file and create dataframes of utdf_geo and utdf_lane
    utdf_dict_data = read_UTDF_file(utdf_filename)
    df_utdf_intersection = generate_intersection_data_from_utdf(utdf_dict_data, city_name)
    utdf_dict_data["utdf_intersection"] = df_utdf_intersection

    # geocoding utdf_intersection
    # df_utdf_geo = generate_coordinates_from_intersection(df_utdf_intersection)

    # store utdf_geo and utdf_lane into utdf_dict_data
    # utdf_dict_data["utdf_geo"] = df_utdf_geo

    # store object into pickle file
    # with open(os.path.join(os.getcwd(), "utdf2gmns.pickle"), 'wb') as f:
    #     pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)

    return utdf_dict_data


@func_running_time
def generate_movement_utdf(input_dir: str = "",
                           city_name: str = "",
                           UTDF_file: str = None,
                           node_file: str = None,
                           movement_file: str = None,
                           output_dir: str = "",
                           isSave2csv: bool = True) -> list:
    """generate_movement_utdf is the main function to generate movement_utdf.csv file

    :param input_dir: defaults to ""
    :type input_dir: str, optional
    :param city_name: defaults to ""
    :type city_name: str, optional
    :param UTDF_file: defaults to None
    :type UTDF_file: str, optional
    :param node_file: defaults to None
    :type node_file: str, optional
    :param movement_file: defaults to None
    :type movement_file: str, optional
    :param output_dir: defaults to "", if not specified, use input directory
    :type output_dir: str, optional
    :param isSave2csv: defaults to True, if True, save the output file to csv file
    :type isSave2csv: bool, optional
    :raises Exception: check if required files exist in the input directory
    :raises Exception: check if coord_x and coord_y are provided in utdf_geo.csv file if it exists
    :raises Exception: save utdf_geo.csv file in the input directory if it does not exist and re-run the function
    :return: a list contain two elements: a dataframe of movement_utdf and a dictionary of utdf_dict_data
    :rtype: list
    """

    # if not specified input_dir, use current working directory
    input_dir = input_dir or os.getcwd()

    # check if required files exist in the input directory
    files_from_directory = get_filenames_from_folder_by_type(input_dir, file_type="csv")

    # if not required, raise an exception
    isRequired = check_required_files_exist(required_files, files_from_directory)
    isRequired_sub = check_required_files_exist(required_files_sub, files_from_directory)

    # required files are not found, raise an exception
    if not isRequired:
        raise Exception(f"Required files {required_files} are not found!")

    # read UTDF file and create dataframes of utdf_intersection and utdf_lane
    path_utdf = path2linux(os.path.join(input_dir, "UTDF.csv"))

    if not city_name:
        print(f"City name is not provided, use default city name {utdf_city_name}")
        print("If you use a different city name, please provide it as a parameter")
        city_name = utdf_city_name

    print("\nStep 1: read UTDF file...")
    utdf_dict_data = generate_utdf_dataframes(path_utdf, city_name)

    # geocoding the utdf_intersection and store it into utdf_dict_data
    # If not automatically geocode, save the utdf_geo.csv file in the input directory
    # And user manually add coord_x and coord_y to in utdf_geo.csv file
    # And re-run the function to generate the final movement_utdf.csv file

    print("Step 1.1: geocoding UTDF intersections from address...")
    # check utdf_geo.csv file existence
    if os.path.exists(path2linux(os.path.join(input_dir, "utdf_geo.csv"))):
        # read utdf_geo.csv file from the input directory
        utdf_dict_data["utdf_geo"] = pd.read_csv(path2linux(
            os.path.join(input_dir, "utdf_geo.csv")))

        # check if user manually added coord_x and coord_y to in utdf_geo.csv file
        if not {"coord_x", "coord_y"}.issubset(set(utdf_dict_data.get("utdf_geo").columns)):
            raise Exception(
                "coord_x or coord_y not found in the utdf_geo.csv file!, please add coord_x and coord_y manually \
                 and re-run the code afterwards."
            )

    # check utdf_geo in utdf_dict_data or not
    # if not generate utdf_geo automatically
    if "utdf_geo" not in utdf_dict_data.keys():
        try:
            # geocoding utdf_intersection automatically
            utdf_dict_data["utdf_geo"] = generate_coordinates_from_intersection(
                utdf_dict_data.get("utdf_intersection"))
        except Exception as e:
            # #  Save the utdf_geo.csv file in the input directory
            utdf_dict_data.get("utdf_intersection").to_csv(
                path2linux(os.path.join(input_dir, "utdf_geo.csv")), index=False)

            raise Exception(
                "We can not geocoding intersections automatically, \
                 We save utdf_geo.csv file in your input dir,   \
                please manually add coord_x and coord_y to the utdf_geo.csv file \
                in your input directory and re-run the code afterwards."
            ) from e

    # required_sub files are not found, will return utdf_intersection and utdf_lane
    if not isRequired_sub:
        print("Because node.csv and movement.csv are not found, \
            the function will return data from utdf in a dictionary, \
            keys are: Lanes, Nodes, Networks, Timeplans, Links and utdf_geo.\n")

        # store object into pickle file
        with open(path2linux(os.path.join(input_dir, "utdf2gmns.pickle")), 'wb') as f:
            pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)
        return utdf_dict_data

    # get the path of each file,
    # since the input directory and files are checked, no need to validate the filename
    print("Step 2: read node.csv and movement.csv (GMNS format)...")
    path_node = path2linux(os.path.join(input_dir, "node.csv"))
    path_movement = path2linux(os.path.join(input_dir, "movement.csv"))

    # read node and movement files
    df_node = pd.read_csv(path_node)
    df_movement = pd.read_csv(path_movement)
    print(f"    : {len(df_node)} nodes loaded.")
    print(f"    : {len(df_movement)} movements loaded.\n")

    # match utdf_intersection_geo with node
    print("Step 3: Performing data merging from GMNS nodes to UTDF intersections based on distance threshold(default 0.1km)...")
    df_intersection_node = match_intersection_node(utdf_dict_data.get("utdf_geo"),
                                                   df_node)

    # match movement with intersection_node
    print("Step 4: Performing data merging from UTDF intersections(geocoded) to GMNS movements based on OSM id...")
    df_movement_intersection = match_movement_and_intersection_node(df_movement,
                                                                    df_intersection_node)

    # match movement with utdf_lane
    print("Step 5: Performing data merging from UTDF Lanes to GMNS movements based on UTDF id...")
    df_movement_utdf_lane = match_movement_utdf_lane(
        df_movement_intersection, utdf_dict_data)

    # match movement with utdf_phase_timeplans
    print("Step 6: Performing data merging from UTDF phases and timeplans to GMNS movements based on UTDF id...")
    df_movement_utdf_phase = match_movement_utdf_phase_timeplans(
        df_movement_utdf_lane, utdf_dict_data)

    # store utdf_intersection_geo and movement_utdf to utdf_dict_data
    utdf_dict_data["movement_utdf_phase"] = df_movement_utdf_phase
    utdf_dict_data["utdf_geo_GMNS_node"] = df_intersection_node

    # save the output file, the default isSave2csv is True
    # if not specified, output path is input directory,
    # output file name = movement_utdf.csv
    if isSave2csv:
        if not output_dir:
            output_dir = input_dir
        output_file_name_1 = validate_filename(os.path.join(output_dir, "movement_utdf.csv"))
        df_movement_utdf_phase.to_csv(output_file_name_1, index=False)

        output_file_name_2 = validate_filename(os.path.join(output_dir, "utdf_intersection.csv"))
        utdf_dict_data.get("utdf_geo").to_csv(output_file_name_2, index=False)

        # with open(path2linux(os.path.join(output_dir, "utdf2gmns.pickle")), 'wb') as f:
        #     pickle.dump(utdf_dict_data, f, pickle.HIGHEST_PROTOCOL)

        print(f" : Successfully saved movement_utdf.csv to: {output_file_name_1}.")
        print(f" : Successfully saved utdf_intersection.csv to: {output_file_name_2}.")

    return [df_movement_utdf_phase, utdf_dict_data]


if __name__ == '__main__':

    city_name = " Bullhead City, AZ"

    # NOTE : the following code is for generating movement_utdf.csv file
    input_dir = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_bullhead_seg4_1"
    df_movement_utdf_phase, utdf_dict_data = generate_movement_utdf(input_dir, city_name, isSave2csv=False)
    # df_movement_utdf_phase.to_csv(path2linux(os.path.join(input_dir, "movement_utdf.csv")), index=False)

    # # NOTE : the following code is for testing purpose only: read utdf.csv file and generate utdf_dict_data
    # path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_ASU_network\UTDF.csv"
    # utdf_dict_data = generate_utdf_dataframes(path_utdf, city_name)
