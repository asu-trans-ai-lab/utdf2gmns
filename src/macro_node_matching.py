import pandas as pd
from math import sin, cos, sqrt, atan2, radians, isnan
import pickle

def CalculateTheDistanceBetweenPoints(x1: float,y1: float,x2: float,y2: float):

    distance = sqrt((x1-x2)**2+(y1-y2)**2)
    return distance


def calculate_point2point_distance_in_km(point1: tuple, point2: tuple) -> float:
    """ point1 and point2: a tuple of (longitude, latitude) """

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1[1])
    lon1 = radians(point1[0])
    lat2 = radians(point2[1])
    lon2 = radians(point2[0])

    dis_lon = lon2 - lon1
    dis_lat = lat2 - lat1

    a = sin(dis_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dis_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # return math.pow((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2, 0.5)

    # the distance is in km
    return distance

if __name__ == '__main__':

    df_interSynchro=pd.read_csv("geo_referencing_lnglat_geocoded.csv")[["full_name","synchro_INTID","x_coord","y_coord","intersection_id"]]
    df_macroNode=pd.read_csv("node.csv")[["node_id","ctrl_type","x_coord","y_coord"]]
    df_macroMovement=pd.read_csv("movement.csv")

    df_match=df_interSynchro.apply(lambda rowIn: df_macroNode.apply((lambda rowMa:CalculateTheDistanceBetweenPoints(rowIn['x_coord'],
                                                                                                                    rowIn['y_coord'],
                                                                                                                    rowMa['x_coord'],
                                                                                                                    rowMa['y_coord'])
    if rowMa["ctrl_type"]=="signal" else -1), axis=1), axis=1)
    df_match.columns=df_macroNode["node_id"]
    maxColumnList=[]
    for index,row in df_match.iterrows():
        flagFindMaxIndex=False
        while not flagFindMaxIndex:
            maxIndex=row.idxmax(axis=0)
            if maxIndex in maxColumnList:
                row[maxIndex]=row[maxIndex]*-1
            else:
                maxColumnList.append(maxIndex)
                flagFindMaxIndex=True

    macroNodeIDSynchroIDDic=dict(zip(maxColumnList, df_interSynchro["synchro_INTID"]))


    df_selected=df_macroMovement.loc[df_macroMovement["node_id"].isin(maxColumnList)]
    columnSynchroList=["full_name","synchro_INTID","x_coord","y_coord","intersection_id"]
    for column in columnSynchroList:
        df_macroMovement.insert(len(df_macroMovement.columns), column, "")
        for index, row in df_selected.iterrows():
            macroNodeID=row["node_id"]
            synchroNodeID=macroNodeIDSynchroIDDic[macroNodeID]
            synchroDataRow=df_interSynchro.loc[df_interSynchro["synchro_INTID"]==synchroNodeID]
            df_macroMovement.loc[index,column]=str(synchroDataRow[column].values[0])



    file= open("globalHashDic.pkl","rb")
    globalHashDic=pickle.load(file)
    file.close()

    from EnumClass import LaneSecondEnum as lase
    laneColumnList=[]
    for i in lase:
        nam = i.name
        if "_" in nam:
            nam = str.replace(nam, "_", " ")
        laneColumnList.append(nam)
        df_macroMovement.insert(len(df_macroMovement.columns),nam,"")

    df_selected=df_macroMovement.loc[df_macroMovement["node_id"].isin(maxColumnList)]

    for index, row in df_selected.iterrows():
        for column in laneColumnList:
            parameterInDifferentDirectionDic=globalHashDic["[Lanes]"][str(macroNodeIDSynchroIDDic[row["node_id"]])][column]
            if parameterInDifferentDirectionDic=={}:
                continue
            else:
                df_macroMovement.loc[index,column]=parameterInDifferentDirectionDic[row["mvmt_txt_id"]]

    df_macroMovement.to_csv("movement_synchro.csv",index=False)
