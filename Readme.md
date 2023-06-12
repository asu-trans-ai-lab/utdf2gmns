## utdf2gmns: Introduction

This open-source package is a tool to conver utdf file to GMNS format.

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

## **Package dependency**:

* [X] geocoder==1.38.1
* [X] numpy==1.23.3
* [X] openpyxl==3.0.10
* [X] pandas==1.4.4

## Data Conversion Steps:

* Step 1: Read UTDF.csv file and perform geocoding, then produce utdf_geo, utdf_lane, and utdf_phase_timeplans.
* Step 2: Match four files (utdf_geo, node, utdf_lane, utdf_pahse_timeplans, movement) to produce movement_utdf

## TODO LIST

* [X] Print out how many intersections being geocoded.
* [ ] Print out how many movements being matched or not matched for signalized intersecton nodes in osm2gmns files.
* [X] Add cycle length and green time for each movement.
* [ ] Check reasonable capacity.
* [ ] Check each movement is reasonable (like 15s of green time...). other attributes.
* [ ] Check number of lanes correctness between osm2gmns file and synchro file per movements.
* [ ] Print out check log.
* [ ] Number of lanes of the movements from synchro file.
* [ ] Add signal info to micre-link.csv
* [ ] Add function to verify whether geocoded for utdf_geo
