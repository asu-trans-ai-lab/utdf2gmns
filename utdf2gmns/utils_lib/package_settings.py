# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, January 27th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

required_files = ["UTDF.csv"]
required_files_sub = ["node.csv", "movement.csv"]

utdf_city_name = " Bullhead, AZ"

utdf_categories = {
    "Network": "Network Settings",
    "Nodes": "Node Data",
    "Links": "Link Data",
    "Lanes": "Lane Group Data",
    "Timeplans": "Timing Plan Settings",
    "Phases": "Phasing Data"}

utdf_metadata = {
    "Nodes":
        """
        INTID: Intersection ID;
        Type: 0 for signalized intersection, 1 for external node, 2 for bend, 3 for unsignalized, 4 for roundabout;
        X, Y, Z: Coordinates of the node, Z is elevation;""",
    "Links":
        """
        INTID: Intersection ID;
        UPID: Upstream node ID;
        Lanes: Number of lanes, for bend or external;
        Distance: travel distance in feet;
        Time: Travel time;
        Speed: Travel speed, mph or km/h;
        Grade: Grade in percent;
        Median: Median width in feet;
        Offset: Offset of link to right of center line, normally zero;
        TWLTL: 1 indicates a TWLTL for link;
        Crosswalk Width: Width of crosswalk at end of link;
        Mandatory and Positioning Distances: For lane change start points;
        Curve Pt X, Pt Y, Pt Z: Used to define a curve point; The other curve point is defined in the reverse link. Blank indicates a straight link;
        """,
    "Lanes": """
        INTID: Intersection ID;
        UPID: Upstream node ID;
        Dest Node: Destination node number for this movement;
        Lanes: For each lane group, enter the number of lanes. Shared lanes count as through lanes, unless there is no through movement, in which case LR lanes count as left lanes.
        Shared: Enter code for sharing of this lane with adjacent movements. This field specified which movements the through lanes are shared with. Enter 0, 1, 2, 3 for No-sharing , shared-with-left, shared-with-right, shared-with-both; This field is normally 0 for turning lane groups. if a left shares with left2 or u-turns. the sharing is coded as 1.

    """

}

utdf_link_column_names = {
    1: 'RECORDNAME',
    2: 'INTID',
    3: 'NB',
    4: 'SB',
    5: "EB",
    6: "WB",
    7: "NE",
    8: "NW",
    9: "SE",
    10: "SW"}

utdf_lane_column_names = {1: 'Up_Node',
                          2: 'Dest_Node',
                          3: 'Lanes',
                          4: 'Shared',
                          5: 'Width',
                          6: 'Storage',
                          7: 'Taper',
                          8: 'StLanes',
                          9: 'Grade',
                          10: 'Speed',
                          11: 'Phase1',
                          12: 'PermPhase1',
                          13: 'LostTime',
                          14: 'Lost_Time_Adjust',
                          15: 'IdealFlow',
                          16: 'SatFlow',
                          17: 'SatFlowPerm',
                          18: 'Allow_RTOR',
                          19: 'SatFlowRTOR',
                          20: 'Volume',
                          21: 'Peds',
                          22: 'Bicycles',
                          23: 'PHF',
                          24: 'Growth',
                          25: 'HeavyVehicles',
                          26: 'BusStops',
                          27: 'Midblock',
                          28: 'Distance',
                          29: 'TravelTime',
                          30: 'Right_Channeled',
                          31: 'Right_Radius',
                          32: 'Add_Lanes',
                          33: 'Alignment',
                          34: 'Enter',
                          35: 'Blocked',
                          36: 'HeadwayFact',
                          37: 'Turning_Speed',
                          38: 'FirstDetect',
                          39: 'LastDetect',
                          40: 'DetectPhase1',
                          41: 'DetectPhase2',
                          42: 'DetectPhase3',
                          43: 'DetectPhase4',
                          44: 'SwitchPhase',
                          45: 'numDetects',
                          46: 'DetectPos1',
                          47: 'DetectSize1',
                          48: 'DetectType1',
                          49: 'DetectExtend1',
                          50: 'DetectQueue1',
                          51: 'DetectDelay1',
                          52: 'DetectPos2',
                          53: 'DetectSize2',
                          54: 'DetectType2',
                          55: 'DetectExtend2',
                          56: 'Exit_Lanes',
                          57: 'CBD',
                          58: 'Lane_Group_Flow'}
