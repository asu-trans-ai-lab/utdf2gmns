# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, November 16th 2022
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from math import sin, cos, sqrt, atan2, radians
import os
import datetime
from pathlib import Path
from typing import Union  # Python version <= 3.9


def func_running_time(func):
    """A decorator to measure the time of a function"""

    def inner(*args, **kwargs):
        print(f'INFO Begin to run function: {func.__name__} …')
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_diff = datetime.datetime.now() - time_start
        print(
            f'INFO Finished running function: {func.__name__}, total: {time_diff.seconds}s')
        print()
        return res
    return inner


# convert OS path to standard linux path
def path2linux(path: str) -> str:
    """Convert OS path to standard linux path

    Parameters
    ----------
    path : str
        the path to be converted

    Returns
    -------
    str
        the converted path
    """

    try:
        return path.replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def get_filenames_from_folder_by_type(dir_name: str, file_type: str = "txt", isTraverseSubdirectory: bool = False) -> list:
    """Get all files in the folder with the specified file type

    Args:
        dir_name (str): the folder path
        file_type (str, optional): the exact file type to specify, if file_type is "*" or "all", return all files in the folder. Defaults to "txt".
        isTraverseSubdirectory (bool, optional): get files inside the subfolder or not, if True, will traverse all subfolders. Defaults to False.

    Returns:
        list: a list of file paths

    Examples:
        # get all files in the folder without traversing subfolder
        >>> from pyhelpers.dirs import get_filenames_from_folder_by_type
        >>> get_filenames_from_folder_by_type("C:/Users/user/Desktop", "txt")
        ['C:/Users/user/Desktop/test.txt']

        # get all files in the folder with traversing subfolder
        >>> from pyhelpers.dirs import get_filenames_from_folder_by_type
        >>> get_filenames_from_folder_by_type("C:/Users/user/Desktop", "txt", isTraverseSubdirectory=True)
        ['C:/Users/user/Desktop/test.txt', 'C:/Users/user/Desktop/sub_folder/test2.txt']
    """

    if isTraverseSubdirectory:
        files_list = []
        for root, dirs, files in os.walk(dir_name):
            files_list.extend([os.path.join(root, file) for file in files])
        if file_type in {"*", "all"}:
            return [path2linux(file) for file in files_list]
        return [path2linux(file) for file in files_list if file.split(".")[-1] == file_type]
    print("input dir:", dir_name, "input file type", file_type)
    # files in the first layer of the folder
    if file_type in {"*", "all"}:
        return [path2linux(os.path.join(dir_name, file)) for file in os.listdir(dir_name)]
    return [path2linux(os.path.join(dir_name, file)) for file in os.listdir(dir_name) if file.split(".")[-1] == file_type]


def check_required_files_exist(required_files: list, dir_files: list) -> bool:
    # format the required file name to standard linux path
    required_files = [path2linux(os.path.abspath(filename)) for filename in required_files]

    required_files_short = [filename.split("/")[-1] for filename in required_files]
    dir_files_short = [filename.split("/")[-1] for filename in dir_files]

    # mask have the same length as required_files
    mask = [file in dir_files_short for file in required_files_short]
    if all(mask):
        return True

    print(f"Error: Required files are not satisfied, \
          missing files are: {[required_files_short[i] for i in range(len(required_files_short)) if not mask[i]]}")

    return False


def validate_filename(path_filename: str, ) -> str:
    """if the file name exist in path,then create new file name with _1, _1_1, ..."""
    filename_abspath = path2linux(os.path.abspath(path_filename))

    file_suffix = filename_abspath.split(".")[-1]
    file_without_suffix = filename_abspath[:-len(file_suffix) - 1]

    if os.path.exists(filename_abspath):
        filename_update = f"{file_without_suffix}_1.{file_suffix}"
        return validate_filename(filename_update)
    return filename_abspath


def calculate_point2point_distance_in_km(point1: tuple, point2: tuple) -> float:
    """ point1 and point2: a tuple of (longitude, latitude) """

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1[1])
    lon1 = radians(point1[0])
    lat2 = radians(point2[1])
    lon2 = radians(point2[0])

    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1

    a = sin(lat_diff / 2)**2 + cos(lat1) * cos(lat2) * sin(lon_diff / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # return math.pow((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2, 0.5)

    # the distance is in km
    return distance


if __name__ == "__main__":
    dir_name = r"C:\Users\roche\Anaconda_workspace\001_Github.com\GTFS2GMNS\test\GTFS"

    # files_from_folder_abspath = get_txt_files_from_folder(dir_name, isTraverseSubdirectory=False)

    # files_required = ["agency.txt", "routes.txt", "shapes.txt", "stops.txt", "trips.txt"]
    # required_files_abspath = [path2linux(os.path.join(dir_name, file)) for file in files_required]

    # isFilesExist = check_required_files_exist(required_files_abspath, files_from_folder_abspath)

    filename = "./node.csv"
    ss = validate_filename("./node.csv")
