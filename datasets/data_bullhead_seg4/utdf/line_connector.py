# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, August 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from shapely.geometry import Point, LineString


def generate_closest_point_connector_wkt(line1_start, line1_end, line2_start, line2_end):
    line1 = LineString([line1_start, line1_end])
    line2 = LineString([line2_start, line2_end])

    closest_point_on_line1 = line1.interpolate(line1.project(line2))
    closest_point_on_line2 = line2.interpolate(line2.project(line1))

    wkt_line_connector = f"LINESTRING ({closest_point_on_line1.x} {closest_point_on_line1.y}, {closest_point_on_line2.x} {closest_point_on_line2.y})"

    return wkt_line_connector


# Example endpoints of two lines (longitude, latitude)
line1_start = (-74.0060, 40.7128)  # Example latitude and longitude
line1_end = (-73.9875, 40.7587)    # Example latitude and longitude
line2_start = (-73.9875, 40.7587)   # Example latitude and longitude
line2_end = (-73.9772, 40.7615)    # Example latitude and longitude

wkt_result = generate_closest_point_connector_wkt(
    line1_start, line1_end, line2_start, line2_end)

print("Generated WKT Line Connector:")
print(wkt_result)
