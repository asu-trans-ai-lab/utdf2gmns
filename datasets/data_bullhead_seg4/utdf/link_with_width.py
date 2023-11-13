# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, August 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import matplotlib.pyplot as plt
from shapely.geometry import LineString


def generate_adjacent_lines_with_width(center_line, width):
    left_line = center_line.parallel_offset(width, 'left')
    right_line = center_line.parallel_offset(-width, 'right')
    return left_line, center_line, right_line


# Example endpoints of a central line (longitude, latitude)
line_start = (-74.0060, 40.7128)  # Example latitude and longitude
line_end = (-73.9772, 40.7615)    # Example latitude and longitude

width = 0.005  # Width of each line in degrees (adjust as needed)

center_line = LineString([line_start, line_end])
left_line, center_line, right_line = generate_adjacent_lines_with_width(
    center_line, width)

# Visualize using Matplotlib
fig, ax = plt.subplots()
ax.plot(*left_line.xy, linewidth=2, color='blue', label='Left Line')
ax.plot(*center_line.xy, linewidth=2, color='green', label='Center Line')
ax.plot(*right_line.xy, linewidth=2, color='red', label='Right Line')

ax.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Adjacent Lines with Width Visualization')
plt.show()


def generate_adjacent_polylines_with_width(center_line, width):
    left_line = center_line.parallel_offset(width, 'left')
    right_line = center_line.parallel_offset(-width, 'right')
    return left_line, center_line, right_line

# Example endpoints of a central polyline (longitude, latitude)
line_vertices = [(-74.0060, 40.7128), (-73.9772, 40.7615), (-73.9550, 40.7290)]  # Example vertices

width = 0.02  # Width of each polyline in degrees (adjust as needed)

center_polyline = LineString(line_vertices)
left_polyline, center_polyline, right_polyline = generate_adjacent_polylines_with_width(center_polyline, width)

# Visualize using Matplotlib
fig, ax = plt.subplots()
ax.plot(*left_polyline.xy, linewidth=2, color='blue', label='Left Polyline')
ax.plot(*center_polyline.xy, linewidth=2, color='green', label='Center Polyline')
ax.plot(*right_polyline.xy, linewidth=2, color='red', label='Right Polyline')

ax.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Adjacent Polylines with Width Visualization')
plt.show()

import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon

def generate_adjacent_polygon_lines(center_line, width):
    left_line = center_line.parallel_offset(width, 'left')
    right_line = center_line.parallel_offset(-width, 'right')

    polygon_vertices = list(left_line.coords) + list(right_line.coords)[::-1]
    polygon = Polygon(polygon_vertices)

    return polygon

# Example endpoints of a central line (longitude, latitude)
line_start = (-74.0060, 40.7128)  # Example latitude and longitude
line_end = (-73.9772, 40.7615)    # Example latitude and longitude

width = 0.01  # Width of each polygon in degrees (adjust as needed)

center_line = LineString([line_start, line_end])
adjacent_polygon = generate_adjacent_polygon_lines(center_line, width)

# Visualize using Matplotlib
fig, ax = plt.subplots()
ax.plot(*center_line.xy, linewidth=2, color='green', label='Center Line')

for polygon in adjacent_polygon:
    x, y = polygon.exterior.xy
    ax.fill(x, y, alpha=0.3)

ax.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Adjacent Polygon Lines Visualization')
plt.show()