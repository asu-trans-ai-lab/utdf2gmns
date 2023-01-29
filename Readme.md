## utdf2gmns: Introduction

This open-source package is a tool to conver utdf file to GMNS format.

## Required Data Input Files:

* [X] UTDF.csv
* [X] node.csv (GMNS format)
* [X] movement.csv (GMNS format)

## **Produced output**

**If input folder have UTDF.csv only:**

* A dictionary store utdf data with keys: Networks, Node, Links, Timeplans, Lanes, and utdf_intersection_geo
* A file named utdf2gmns.pickle to store dictionary object.

**If input folder have node.csv and movement.csv:**

* Two files named movement_utdf.csv and intersection_utdf.csv
* A file named utdf2gmns.pickle to store dictionary object.

## **Package dependency**:

* [X] geocoder==1.38.1
* [X] numpy==1.23.3
* [X] openpyxl==3.0.10
* [X] pandas==1.4.4

## Data Conversion Steps:

* Step 1: Read UTDF.csv file and perform geocoding, then produce utdf_geo and utdf_lane.
* Step 2: Match four files (utdf_geo, node, utdf_lane, movement) to produce movement_utdf
