## utdf2gmns

## Introduction

This open-source package is a tool to convert utdf file to GMNS format.

## Required Data Input Files:

* [X] UTDF.csv
* [X] node.csv (GMNS format)
* [X] movement.csv (GMNS format)

## **Produced outputs**

**If input folder have UTDF.csv only, outputs are:**

* A dictionary store utdf data with keys: Networks, Node, Links, Timeplans, Lanes, and utdf_intersection_geo
* A file named utdf2gmns.pickle to store dictionary object.

**If input folder have extra node.csv and movement.csv, outputs are:**

* Two files named movement_utdf.csv and intersection_utdf.csv
* A file named utdf2gmns.pickle to store dictionary object.

## **Package dependencies**:

* [X] geocoder==1.38.1
* [X] numpy==1.23.3
* [X] openpyxl==3.0.10
* [X] pandas==1.4.4

## Data Conversion Steps:

Step 1: Read UTDF.csv file and perform geocoding, then produce utdf_geo, utdf_lane, and utdf_phase_timeplans.

Step 2: Match four files (utdf_geo, node, utdf_lane, utdf_pahse_timeplans, movement) to produce movement_utdf

## Installation

`pip install UTDF2GMNS`

## Example

```python
import utdf2gmns as ug
import pandas as pd
if__name__=="main":
    city =" Bullhead City, AZ"
    # option= 1, generate movement_utdf.csv directly
    # option= 2, generate movement_utdf.csv step by step (more flexible)

    option =1

    if option ==1:
        # NOTE: Option 1, generate movement_utdf.csv directly
        path =r"C:\Users\roche\Desktop\coding\data_bullhead_seg4"  # the fold contain UTDF.csv, node.csv and movement.csv
        res = ug.generate_movement_utdf(path, city,isSave2csv=True)

    if option ==2:
        # NOTE: Option 2, generate movement_utdf.csv step by step (more flexible)
        path_utdf =r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\UTDF.csv"
        path_node =r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\node.csv"
        path_movement =r"C:\Users\roche\Desktop\coding\data_bullhead_seg4\movement.csv"

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

```

## TODO LIST

* [X] Print out how many intersections being geocoded.
* [ ] Print out how many movements being matched or not matched for signalized intersecton nodes in osm2gmns files.
* [ ] Add cycle length and green time for each movement.
* [ ] Check reasonable capacity.
* [ ] Check each movement is reasonable (like 15s of green time...). other attributes.
* [ ] Check number of lanes correctness between osm2gmns file and synchro file per movements.
* [X] Print out check log.
* [X] Number of lanes of the movements from synchro file.
* [ ] Add signal info to micre-link.csv
* [X] Add function to verify whether geocoded for utdf_geo
