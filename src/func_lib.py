# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, January 17th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import pandas as pd
from utility_lib import utdf_categories

def read_UTDF_file(filename: str) -> dict:
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


if __name__ == '__main__':
    path_utdf = r"C:\Users\roche\Anaconda_workspace\001_Github\utdf2gmns\dataset\UTDF.csv"

    utdf_categories_data_dict = read_UTDF_file(path_utdf)





