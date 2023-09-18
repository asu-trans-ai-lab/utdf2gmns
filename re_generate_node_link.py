# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, September 18th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import osm2gmns as og

net = og.getNetFromFile("./datasets/data_Tempe_network/tempe.osm.pbf", POI=True)

# og.outputNetToCSV(net)

og.consolidateComplexIntersections(net, auto_identify=True)
og.outputNetToCSV(net)



net = og.getNetFromFile("./datasets/data_Tempe_network/tempe.osm.pbf", default_lanes=True)
og.consolidateComplexIntersections(net, auto_identify=True)
og.buildMultiResolutionNets(net)
og.outputNetToCSV(net)
