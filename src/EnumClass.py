from enum import Enum

class NetworkEnum(Enum):
    RECORDNAME=1
    DATA=2

class NetworkSecondEnum(Enum):
    UTDFVERSION=1
    Metric=2
    yellowTime=3
    allRedTime=4
    Walk=5
    DontWalk=6
    HV=7
    PHF=8
    DefWidth=9
    DefFlow=10
    vehLength=11
    heavyvehlength=12
    criticalgap=13
    followuptime=14
    stopthresholdspeed=15
    criticalmergegap=16
    growth=17
    PedSpeed=18
    LostTimeAdjust=19
    ScenarioDate=20


class NodeEnum(Enum):
    INTID =1
    TYPE =2
    X =3
    Y =4
    Z =5
    DESCRIPTION =6
    CBD =7
    Inside_Radius =8
    Outside_Radius =9
    Roundabout_Lanes = 10
    Circle_Speed= 11

class LinkEnum(Enum):
    RECORDNAME =1
    INTID = 2
    NB=3
    SB=4
    EB=5
    WB=6
    NE=7
    NW=8
    SE=9
    SW=10

class LinkSecondEnum(Enum):
    Up_ID =1
    Lanes =2
    Name =3
    Distance =4
    Speed=5
    Time =6
    Grade =7
    Median =8
    Offset =9
    TWLTL =10
    Crosswalk_Width =11
    Mandatory_Distance =12
    Mandatory_Distance2 =13
    Positioning_Distance =14
    Positioning_Distance2 =15
    Curve_Pt_X =16
    Curve_Pt_Y =17
    Curve_Pt_Z =18
    Link_Is_Hidden =19
    Street_Name_Is_Hidden =20

class LaneEnum(Enum):
    RECORDNAME=1
    INTID=2
    NBL=3
    NBT=4
    NBR=5
    SBL=6
    SBT=7
    SBR=8
    EBL=9
    EBT=10
    EBR=11
    WBL=12
    WBT=13
    WBR=14
    NEL=15
    NET=16
    NER=17
    NWL=18
    NWT=19
    NWR=20
    SEL=21
    SET=22
    SER=23
    SWL=24
    SWT=25
    SWR=26
    PED=27
    HOLD=28

class LaneSecondEnum(Enum):
    Up_Node=1
    Dest_Node=2
    Lanes=3
    Shared=4
    Width=5
    Storage=6
    Taper=7
    StLanes=8
    Grade=9
    Speed=10
    Phase1=11
    PermPhase1=12
    LostTime=13
    Lost_Time_Adjust=14
    IdealFlow=15
    SatFlow=16
    SatFlowPerm=17
    Allow_RTOR=18
    SatFlowRTOR=19
    Volume=20
    Peds=21
    Bicycles=22
    PHF=23
    Growth=24
    HeavyVehicles=25
    BusStops=26
    Midblock=27
    Distance=28
    TravelTime=29
    Right_Channeled=30
    Right_Radius=31
    Add_Lanes=32
    Alignment=33
    Enter=34
    Blocked=35
    HeadwayFact=36
    Turning_Speed=37
    FirstDetect=38
    LastDetect=39
    DetectPhase1=40
    DetectPhase2=41
    DetectPhase3=42
    DetectPhase4=43
    SwitchPhase=44
    numDetects=45
    DetectPos1=46
    DetectSize1=47
    DetectType1=48
    DetectExtend1=49
    DetectQueue1=50
    DetectDelay1=51
    DetectPos2=52
    DetectSize2=53
    DetectType2=54
    DetectExtend2=55
    Exit_Lanes=56
    CBD=57
    Lane_Group_Flow=58

class TimeplanEnum(Enum):
    RECORDNAME=1
    INTID=2
    DATA=3

class TimeplanSecondEnum(Enum):
    Control_Type=1
    Cycle_Length=2
    Lock_Timings=3
    Referenced_To=4
    Reference_Phase=5
    Offset=6
    Master=7
    Yield=8
    Node_0=9
    Node_1=10

class PhaseEnum(Enum):
    RECORDNAME=1
    INTID=2
    D1=3
    D2=4
    D3=5
    D4=6
    D5=7
    D6=8
    D7=9
    D8=10

class PhaseSecondEnum(Enum):
    BRP=1
    MinGreen=2
    MaxGreen=3
    VehExt=4
    TimeBeforeReduce=5
    TimeToReduce=6
    MinGap=7
    Yellow=8
    AllRed=9
    Recall=10
    Walk=11
    DontWalk=12
    PedCalls=13
    MinSplit=14
    DualEntry=15
    InhibitMax=16
    Start=17
    End=18
    Yield=19
    Yield170=20
    LocalStart=21
    LocalYield=22
    LocalYield170=23
    ActGreen=24
