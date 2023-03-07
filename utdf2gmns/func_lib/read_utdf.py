# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, January 17th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# from utility_lib import func_running_time
import pandas as pd
import sys
import os
from pathlib import Path

# add folder utils_lib to the path
try:
    sys.path.append(os.path.join(Path(__file__).resolve().parent.parent, "utils_lib"))
except Exception:
    sys.path.append(os.path.join(Path("__file__").resolve().parent.parent, "utils_lib"))

try:
    # for deployment
    from utils_lib.package_settings import link_column_names, utdf_categories, utdf_setting
    from utils_lib.utility_lib import func_running_time
except Exception:
    # for local testing
    from package_settings import link_column_names, utdf_categories, utdf_setting
    from utility_lib import func_running_time

# aviod the warning of "A value is trying to be set on a copy of a slice from a DataFrame"
pd.options.mode.chained_assignment = None  # default='warn'

@func_running_time
def read_UTDF_file(path_utdf: str) -> dict:
    """ read UTDF file and split data into different categories """

    # read the utdf.csv file
    with open(path_utdf, encoding='utf-8') as f:
        lines = f.readlines()

    # find the start index of each category, the index is the row contain column names
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
    utdf_dict_data = {}

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
        utdf_dict_data[category_name] = pd.DataFrame(category_value[1:], columns=category_value[0])

    # format utdf_lane data : remove unnecessary rows with None and column with '\n'
    # format each table in utdf_dict_data
    for table_name, df_table_name in utdf_dict_data.items():
        try:
            # get the last column name from utdf_setting
            last_col_name = list(df_table_name.columns)[-1]

            # remove unnecessary rows / invalid rows with NaN
            if table_name != "Network":
                df_table_name = df_table_name[df_table_name["INTID"].notna()]
                df_table_name = df_table_name[df_table_name['INTID'].astype(str).str.isdigit()]
            else:
                df_table_name = df_table_name[df_table_name[last_col_name].notna()]

            # clean the data / remove '\n' in the end of column SW


            df_table_name.loc[:, last_col_name] = df_table_name[last_col_name].map(
                lambda x: x.replace("\n", ""))

            df_table_name = df_table_name.rename(columns={last_col_name: last_col_name.replace("\n", "")})

            utdf_dict_data[table_name] = df_table_name
        except Exception as e:
            print(f"Could not format table: {table_name} for {e}")
            continue

    utdf_dict_data["phase_timePlans"] = pd.concat([utdf_dict_data["Phases"], utdf_dict_data["Timeplans"]], axis=0, ignore_index=True)
    return utdf_dict_data


@func_running_time
def generate_intersection_data_from_utdf(utdf_dict_data: dict, city_name: str) -> pd.DataFrame:

    # Get link data from utdf
    df_link = utdf_dict_data["Links"]

    # update columns name
    df_link.columns = [i.replace("\n", "") if "\n" in i else i for i in df_link.columns.tolist()]

    # remove unnecessary rows / invalid rows with NaN
    df_link = df_link[df_link["INTID"].notna()]

    # clean the data / remove '\n' in the end of column SW
    # df_link = df_link.rename(columns={"SW\n": "SW"})
    # df_link["SW"] = df_link["SW"].map(lambda x: x.replace("\n", ""))

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
            df_single_id_name = df_single_id[df_single_id["RECORDNAME"] == name].to_dict("records")[0]
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
            direction_name = direction_list.get(link_column_names.get(direction_id), "")
            if direction_name not in direction_name_list and direction_name != '' and direction_name != '\n':
                direction_name_list.append(direction_name)
        if len(direction_name_list) > 1:
            isIntersection = True

        intersection_name = ""
        if isIntersection:
            intersection_name = ' & '.join(direction_name_list)
            # get "INTID"
            intersection_id = direction_list[link_column_names.get(2)]

            link_list.append([intersection_name, city_name, intersection_id, "", sequenced_intersection_id])
            sequenced_intersection_id += 1

    intersection_column_name = ["intersection_name", "city_name",
                                "synchro_INTID", "file_name", "intersection_id"]
    df_utdf_intersection = pd.DataFrame(link_list, columns=intersection_column_name)
    df_utdf_intersection["intersection_name"] = df_utdf_intersection["intersection_name"].map(lambda x: x.replace("\n", ""))

    return df_utdf_intersection


if __name__ == '__main__':
    path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_bullhead_seg4\UTDF.csv"
    # path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\datasets\data_test_1\UTDF.csv"

    city_name = utdf_setting.get("city_name")

    utdf_dict_data = read_UTDF_file(path_utdf)
