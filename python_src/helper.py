from Configuration import ConfigHolder
from pathlib import Path
import json
import subprocess
import os
import shutil
import numpy as np

cfgHolder = ConfigHolder()
config = cfgHolder.get()
prefixLIST = config['path_prefix']['AC_plugin_LIST']
prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
prefixDATA = config['path_prefix']['AC_DATA']
prefixDotPROBACK = config['path_prefix']['dotPRO']


def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True


def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b




def copyDotPROFile(fileName):

    # find source file path
    sourceFilePath = Path(prefixLIST + fileName).resolve()
    soruceFile = Path(sourceFilePath)

    # Generate target file path
    targetFilePath = prefixDotPROBACK + fileName + '.BACK'
    targetFile = Path(targetFilePath)

    # check file source is exist and file target is not exist
    if soruceFile.is_file() and not targetFile.is_file():
        shutil.copy2(sourceFilePath, targetFilePath)

def readDotPROFile(fileName):

    configList = []
    lineCnt = 0
    sourceFilePath = Path(prefixLIST + fileName).resolve()

    with open(sourceFilePath, 'r') as f:
        for line in f.readlines():

            if lineCnt >= 26:
                break
            if line is not "\n":
                el = line.split(':')[0].strip()
                if isfloat(el):
                    configList.append(float(el))
                elif isint(el):
                    configList.append(int(el))

            lineCnt = lineCnt + 1
    f.close()
    return configList


def replaceDotPRObyLine(fileName, lineNum, contentStr):
    # lineNum is start with index = 0

    sourceFilePath = Path(prefixLIST + fileName).resolve()

    f = open(sourceFilePath, 'r+')

    lines = f.readlines()
    # ensure the lineNum should be existed contents
    if lineNum < len(lines):
        seg2 = lines[lineNum].split(':')[1]
        lines[lineNum] = contentStr + ' : ' + seg2
        # print ( lines[lineNum] )
    f.close()
    out = open(sourceFilePath, 'w')
    out.writelines(lines)
    out.close()


def appendDotIRR(fileName, day, irriAmount):

    sourceFilePath = Path(prefixDATA + fileName).resolve()
    with open(sourceFilePath, 'a') as f:
        irriEventStr = '\n{:6d} {:9.1f} {:12.1f}'.format(day, irriAmount, 0)
        f.write(irriEventStr)





def mockControllerBySI(wc_shallow, ref1=25):

    kp = 1.5
    ki = 0
    kd = 0

    e1 = ref1 - wc_shallow

    irri = e1 * kp

    if irri < 0:
        irri = 0
    elif irri > 120:
        irri = 120

    return irri

# EWZ = Efficient Wetting Zone


def ETbasedIrrigation(ET, k):
    return ET * k


def calEWZbyCompartment(compartmentBoundary, depth):
    closestIdx = min(range(len(compartmentBoundary)),
                     key=lambda i: abs(compartmentBoundary[i] - depth))
    return compartmentBoundary[closestIdx]


def writeDayData2AlignedCSV(absSource, absDestination):

    # first line is meta-data,
    # Second line is blank
    # Third line is unit of column
    dataCSV = []
    with open(absSource, 'r') as fin:

        COLUMN_SKIP_LINE_NUM = config['day_data_format']['COLUMN_SKIP_LINE_NUM']
        COLUMN_UNIT_LINE_NUM = config['day_data_format']['COLUMN_UNIT_LINE_NUM']
        data = fin.readlines()
        rowCount = 1
        for line in data:

            # if rowCount > 5:
            #     break

            seg = [ele for ele in line.split(' ') if ele != '']

            if rowCount == COLUMN_UNIT_LINE_NUM:
                missingUnitList = config['day_data_format']['missingUnits']
                seg = missingUnitList + seg

            segCSV = ','.join(seg)
            dataCSV.append(segCSV)
            rowCount = rowCount + 1

    with open(absDestination, 'w') as fout:
        for line in dataCSV:
            fout.write(line)


def writeSeasonData2AlignedCSV(absSource, absDestination):

    # first line is meta-data,
    # Second line is blank
    # Third line is unti of column

    dataCSV = []
    with open(absSource, 'r') as fin:

        COLUMN_SKIP_LINE_NUM = config['day_data_format']['COLUMN_SKIP_LINE_NUM']
        COLUMN_UNIT_LINE_NUM = config['day_data_format']['COLUMN_UNIT_LINE_NUM']
        data = fin.readlines()
        rowCount = 1
        for line in data:
            # if rowCount > 5:
            #     break

            seg = [ele for ele in line.split(' ') if ele != '']

            if rowCount == COLUMN_UNIT_LINE_NUM:
                missingUnitList = config['season_data_format']['missingUnits']
                seg = missingUnitList + seg

            segCSV = ','.join(seg)
            dataCSV.append(segCSV)
            rowCount = rowCount + 1

    with open(absDestination, 'w') as fout:
        for line in dataCSV:
            fout.write(line)


def generateDotOUTName(name):
    OUTExt = '.OUT'
    dotOUTName = name + 'PROday' + OUTExt
    return dotOUTName


def generateDotPROName(name):

    PROExt = '.PRO'
    dotPROName = name + PROExt
    return dotPROName


def extractYieldandTotalIrri(simulationName):
    prefixOutput = config['path_prefix']['output']
    HEADER_NUM = config['day_data_format']['HEADER_ROW_NUM']
    seasonIrriIndex = 8
    seasonYield = 30
    fileType = 'season'
    path = str(
        Path(prefixOutput + r'{}_{}.csv'.format(simulationName, fileType)).resolve())

    # load simulation result
    # dailyData = np.loadtxt( path, skiprows=HEADER_NUM, delimiter="," )
    # dailyDataArray = np.array( dailyData )
    # print(dailyDataArray)
    colsDefString = "Period	Day1	Month1	Year1	Rain	ETo	GD	CO2	Irri	Infilt	Runoff	Drain	Upflow	E	E/Ex	Tr	Tr/Trx	SaltIn	SaltOut	SaltUp	SaltProf	Cycle	SaltStr	FertStr	TempStr	ExpStr	StoStr	BioMass	Brelative	HI	Yield	WPet	DayN	MonthN	YearN	File"
    colsDefTuple = tuple(colsDefString.split('\t'))
    dailyData = np.genfromtxt(
        path, delimiter=',', skip_header=HEADER_NUM, dtype=float, names=colsDefTuple)

    seasonIrri = dailyData[colsDefTuple[seasonIrriIndex]][-1]
    seasonYield = dailyData[colsDefTuple[seasonYield]][-1]
    return {'seasonIrri': seasonIrri, 'seasonYield': seasonYield}


def writeResultList(resultList):
    prefixOutput = config['path_prefix']['output']
    path = str(Path(prefixOutput + r'result.csv').resolve())
    with open(path, 'a') as f:
        for result in resultList:
            line = '{:d},{:d},{:f},{:f}\n'.format(
                result['depth'], result['ref'], result['seasonYield'], result['seasonIrri'])
            f.write(line)


def writeMovingResultList(resultList):
    
    prefixOutput = config['path_prefix']['output']
    path = str(Path(prefixOutput + r'result.csv').resolve())
    with open(path, 'a') as f:
        for result in resultList:
            line = '{:f},{:d},{:f},{:f}\n'.format(
                result['mp'], result['ref'], result['seasonYield'], result['seasonIrri'])
            f.write(line)


def readSharedInfo(path):
    sharedInfo = {}
    with open(path, "r") as data:
        sharedInfo = json.load(data)

    return sharedInfo


def increaseIdSharedInfo(path):

    sharedInfo = {}
    with open(path, "r") as data:
        sharedInfo = json.load(data)

    with open(path, "r+", encoding='utf-8') as data:
        sharedInfo["current_unique_id"] = sharedInfo["current_unique_id"] + 1
        json.dump(sharedInfo, data, indent=4)


def writeAlgorithmStatus(statusList):
    prefixOutput = config['path_prefix']['output']
    path = str(Path(prefixOutput + r'result.csv').resolve())
    with open(path, 'a') as f:
        for result in resultList:
            line = '{:d},{:d},{:f},{:f}\n'.format(
                result['depth'], result['ref'], result['seasonYield'], result['seasonIrri'])
            f.write(line)
# def createExpJSON(srcPath, destPath):
#     sharedInfo = readSharedInfo(srcPath)
#     with open(destPath, "r+") as outfile:
#         json.dump(sharedInfo["info_format"], data, indent=4).encode("uff_8")
