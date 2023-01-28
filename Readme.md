## utdf2gmns: Introduction

This open-source package is a tool to conver utdf file to GMNS format.

## Require documents:

* [X] UTDF.csv
* [X] node.csv
* [X] movement.csv

## **Package dependency**:

* [X] geocoder==1.38.1
* [X] numpy==1.23.3
* [X] openpyxl==3.0.10
* [X] pandas==1.4.4

## Project logic:

* Step1: Check all required documents exists in the input directory, else, raise an exception
* Step2: Read UTDF.csv file to get data of utdf_intersection and utdf_lane
* Step3: Read node and movement documents
* Step4: Geocoding utdf_intersection, add two columns: coord_x and coord_y -> utdf_intersection_geo
* Step5: Match utdf_intersection_geo and node -> utdf_intersection_node
* Step6: Match movement and utdf_intersection_node -> movement_intersection
* Step7: Match movement_intersection and utdf_lane  -> movement_utdf

### Georeferencing Code Logic (Step4)

**Three-way validation**

* Step1: calculate result_1(longitude and latitude) using intersection_name and city_name (eg. SR95 & Aviation, Bullhead, AZ)
* Step2: calculate result_2(longitude and latitude) using **reversed** intersection_name and city_name (eg. Aviation & SR95, Bullhead, AZ)

If results of step1 and step2 are same, use result_1(longitude and latitude) and finish.

If results are not equal:

    if the distance between result_1 and result_2 within the threshould, use result_1 and finish

    else, use three-points-validation-methods to generate longitude and latitude.
