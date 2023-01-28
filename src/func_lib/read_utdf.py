# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, January 17th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from package_settings import link_column_names, utdf_setting, utdf_categories
import pandas as pd


def read_UTDF_file(path_utdf: str) -> dict:
    """ read UTDF file and split data into different categories """

    # read the utdf.csv file
    with open(path_utdf, encoding='utf-8') as f:
        lines = f.readlines()

    # find the start index of each category, the index is the column name
    categorical_data_beginning_index_dict = {}
    for i in range(len(lines)):
        if "Network" in lines[i] and utdf_categories["Network"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Network"
        elif "Nodes" in lines[i] and utdf_categories["Nodes"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Nodes"
        elif "Links" in lines[i] and utdf_categories["Links"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Links"
        elif "Lanes" in lines[i] and utdf_categories["Lanes"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Lanes"
        elif "Timeplans" in lines[i] and utdf_categories["Timeplans"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Timeplans"
        elif "Phases" in lines[i] and utdf_categories["Phases"] in lines[i + 1]:
            categorical_data_beginning_index_dict[i+2] = "Phases"
        else:
            continue

    categorical_index_ordered = sorted(list(categorical_data_beginning_index_dict.keys())) # ascending order

    # prepare dataframe for each category
    utdf_categories_data_dict = {}

    for j in range(len(categorical_index_ordered)):
        # get the category name from start_index_dict
        category_name  = categorical_data_beginning_index_dict[categorical_index_ordered[j]]

        # if it's the last value in the list, then the end index is the end of the file
        if j == len(categorical_index_ordered) - 1:
            category_value = [k.split(",") for k in lines[categorical_index_ordered[j]:]]

        # if it's not the last value in the list, then the end index is the start index of the next category - 2
        else:
            category_value = [k.split(",") for k in lines[categorical_index_ordered[j]:categorical_index_ordered[j+1] - 2]]

        # save data to dictionary
        utdf_categories_data_dict[category_name] = pd.DataFrame(category_value[1:], columns=category_value[0])
    return utdf_categories_data_dict


def generate_intersection_data_from_utdf(utdf_dict_data: dict) -> pd.DataFrame:

    # Get link data from utdf
    df_link = utdf_dict_data["Links"]

    # remove unnecessary rows / invalid rows with NaN
    df_link = df_link[df_link["INTID"].notna()]

    # clean the data / remove '\n' in the end of column SW
    df_link = df_link.rename(columns={"SW\n": "SW"})
    df_link["SW"] = df_link["SW"].map(lambda x: x.replace("\n", ""))

    # get the unique link id
    link_id = df_link["INTID"].unique().tolist()

    # generate link dictionary in format of: {link_id: {RECORDNAME:{columns:values}}}
    df_link_dict = {}
    for single_id in link_id:
        df_single_id = df_link[df_link["INTID"] == single_id]
        record_name = df_single_id["RECORDNAME"].unique().tolist()
        df_single_id_dict = {}
        for name in record_name:
            # convert one row of dataframe to dictionary
            df_single_id_name = df_single_id[df_single_id["RECORDNAME"] == name].to_dict("records")[
                0]
            df_single_id_dict[name] = df_single_id_name
        df_link_dict[single_id] = df_single_id_dict

    # prepare intersection dataframe
    sequenced_intersection_id = 0
    link_list = []

    # for each single link id
    for single_id in df_link_dict:
        # define a flag to indicate whether an intersection exists
        isIntersection = False

        direction_list = df_link_dict[single_id]["Name"]
        direction_name_list = []
        for direction_id in range(3, 11):
            direction_name = direction_list[link_column_names.get(
                direction_id)]
            if direction_name not in direction_name_list and direction_name != '':
                direction_name_list.append(direction_name)
        if len(direction_name_list) > 1:
            isIntersection = True

        intersection_name = ""
        if isIntersection:
            intersection_name = ' & '.join(direction_name_list)
            # get "INTID"
            intersection_id = direction_list[link_column_names.get(2)]

            link_list.append([intersection_name, utdf_setting.get(
                "city_name"), intersection_id, "", sequenced_intersection_id])
            sequenced_intersection_id += 1

    intersection_column_name = ["intersection_name", "city_name",
                                "synchro_INTID", "file_name", "intersection_id"]
    return pd.DataFrame(link_list, columns=intersection_column_name)


def generate_lane_data_from_utdf(utdf_dict_data: dict) -> pd.DataFrame:

    # Get link data from utdf
    df_lane = utdf_dict_data["Lanes"]

    # remove unnecessary rows / invalid rows with NaN
    df_lane = df_lane[df_lane["INTID"].notna()]

    # clean the data / remove '\n' in the end of column SW
    df_lane = df_lane.rename(columns={"HOLD\n": "HOLD"})
    df_lane["HOLD"] = df_lane["HOLD"].map(lambda x: x.replace("\n", ""))
    return df_lane


if __name__ == '__main__':
    path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1\UTDF.csv"

    utdf_dict_data = read_UTDF_file(path_utdf)

    df_intersection = generate_intersection_data_from_utdf(utdf_dict_data)

    df_lane = generate_lane_data_from_utdf(utdf_dict_data)






