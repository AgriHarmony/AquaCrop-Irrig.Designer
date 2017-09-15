import numpy as np
import helper as helper
import datetime
import subprocess
from settings import ConfigHolder
from pathlib import Path

# Configuration
cfgHolder = ConfigHolder()
config = cfgHolder.get()
prefixLIST = config['path_prefix']['AC_plugin_LIST']
prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
prefixIRR = config['path_prefix']['AC_DATA']
prefixOutput = config['path_prefix']['output']

class EnvSimulator():
    
    def __init__(self, name=""):
        
        self.dailyData = None

        # Initialize directory and path
        self.name = name
        self.dotPROName = helper.generateDotPROName(self.name)
        self.dotOUTName = helper.generateDotOUTName(self.name)
         
        self.firstSimuDay = 0
        self.lastSimuDay = 0
        self.firstCropDay = 0
        self.lastCropDay = 0
        
        # Initilize simulation day information
        self.readPROfile()
        
        # the pointer for reading current read dailyData, index start from 0
        self.dailyDataPointer = 0
        # the count of current simulation day
        self.currentSimuDay = 0
        self.currentSimuDay = self.firstSimuDay
        self.currentDayCount = 1

    def runOnce(self):
        pluginExeLocation = config['executable_path']
        subprocess.call([pluginExeLocation])

    def initRun(self):
        """
            Do First Simulation to generate whole moisture(VWC) variation, this should be refactoring
        """
        helper.cleanExampleDotIrrFile()
        helper.executeAquaCropPlugin()
        self.loadResult()

    def readPROfile(self):
        # Store the end of simu-day to variable to control simulation loop
        dotPROList = helper.readDotPROFile(self.dotPROName)
        # print( dotPROList )

        self.firstSimuDay = int(dotPROList[1])
        self.lastSimuDay = int(dotPROList[2])
        self.firstCropDay = int(dotPROList[3])
        self.lastCropDay = int(dotPROList[4])
        # print( 'firstSimuDay:{}'.format( firstSimuDay ) )
            # print( 'lastSimuDay:{}'.format( lastSimuDay ) )
    
    def getIrrigationHistory(self):
        irrIdx=config['day_data_index']['irrigation']
        return self.dailyData[:,irrIdx]
    
    def getETHistory(self):
        ETIdx=config['day_data_index']['ET']
        return self.dailyData[:,ETIdx]
    
    def getAllDailyData(self):
        return self.dailyData

    def loadResult(self):
        prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
        pathOUT = prefixOUTP + self.dotOUTName
        dailyData = np.loadtxt(pathOUT, skiprows=4)
        self.dailyData =  dailyData

    def isFinish(self):
        if self.currentSimuDay == self.lastSimuDay:
            return True
        else:
            return False
    def getCurrentDayWCs(self):
        wcStartIdx=config['day_data_index']['wc1']
        wcEndIdx=config['day_data_index']['wc1']+7
        return self.dailyData[self.dailyDataPointer,wcStartIdx:wcEndIdx]

    def getCurrentDayData(self):
        return self.dailyData[self.dailyDataPointer,:]

    def getCurrentRootDepth(self):
        currentDayData = self.dailyData[:,self.dailyDataPointer]
        return currentDayData[config['day_data_index']['zoot']]

    def increateTimeStep(self):
        self.currentSimuDay = self.currentSimuDay + 1
        self.dailyDataPointer = self.dailyDataPointer + 1
        self.currentDayCount = self.currentDayCount + 1
    
    def buildOUTSorucePath(self, fileType, sourcePROName ):
        return Path(prefixOUTP + r'{}PRO{}.OUT'.format(sourcePROName, fileType) ).resolve()
    
    def buildOUTDestPath(self, fileType, simulationName ):
        return Path(prefixOutput + r'{}_{}.csv'.format(simulationName, fileType) ).resolve()

    def writeOutResult(self, sourcePROName, simulationName):
        # copy file and write to specific location
        daySource = self.buildOUTSorucePath('day', sourcePROName)
        dayDest = self.buildOUTDestPath('day', simulationName)
        helper.writeDayData2AlignedCSV(str(daySource),str(dayDest))

        seasonSource = self.buildOUTSorucePath('season', sourcePROName)
        seasonDest = self.buildOUTDestPath('season', simulationName)
        helper.writeSeasonData2AlignedCSV(str(seasonSource), str(seasonDest))