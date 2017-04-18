
import subprocess
import os
import numpy as np

from pathlib import Path

prefix = '../bin/aquacrop_plug_in_v5_0/LIST/'
prefixOUT = '../bin/aquacrop_plug_in_v5_0/OUTP/'
prefixIRR = '../bin/aquacrop_v5_0/DATA/'


# Location
pluginExeLocation = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\ACsaV50.exe'

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

def copyDotPROFile( fileName ):
    
    # find source file path
    sourceFilePath = Path( prefix+fileName ).resolve()
    soruceFile = Path( sourceFilePath )
    
    # Generate target file path
    parentDirPath = os.path.dirname ( sourceFilePath )
    targetFilePath = parentDirPath + '/' + fileName + '.BACK'
    targetFile = Path( targetFilePath )

    # check file source is exist and file target is not exist 
    if soruceFile.is_file() and not targetFile.is_file():
        os.system( 'cp {} {}'.format(sourceFilePath, targetFilePath) )


def readDotPROFile( fileName ):
    
    configList = []
    lineCnt = 0
    sourceFilePath = Path(prefix+fileName).resolve()
    
    with open( sourceFilePath, 'r' ) as f:
        for line in f.readlines():
            
            if lineCnt >= 26:
                break
            if line is not "\n":
                el = line.split(':')[0].strip();
                if isfloat( el ):
                    configList.append( float( el ) )
                elif isint( el ):
                    configList.append( int( el ) )  
        
               
            lineCnt = lineCnt + 1;
    f.close()
    return configList

def replaceDotPRObyLine( fileName, lineNum, contentStr ):
    # lineNum is start with index = 0

    sourceFilePath = Path(prefix+fileName).resolve()
    print ( sourceFilePath )
    f = open( sourceFilePath, 'r+' )
    
    lines = f.readlines()
    # ensure the lineNum should be existed contents
    if lineNum < len(lines) :
        seg2 = lines[lineNum].split(':')[1] 
        lines[lineNum] = contentStr + ' : ' +  seg2
        # print ( lines[lineNum] )
    f.close()
    out = open( sourceFilePath, 'w' )
    out.writelines( lines )
    out.close()
def appendDotIRR( fileName, day, irriAmount ):
    
    sourceFilePath = Path( prefixIRR + fileName ).resolve()
    print ( sourceFilePath )

    with open( sourceFilePath, 'a') as f:
        irriEventStr = '\n{:6d} {:9.1f} {:12.1f}'.format( day, irriAmount, 0)
        f.write( irriEventStr )
def executeAquaCropPlugin():
     subprocess.call([pluginExeLocation])

def mockControllerBySI( wc1, wc2 ):

    kp = 1.5
    ki = 0
    kd = 0

    ref1 = 25
    ref2 = 17

    e1 = ref1 - wc1
    e2 = ref2 - wc2

    irri = e1*kp

    if irri < 0:
        irri = 0
    elif irri > 120:
        irri = 120

    return irri

     
if __name__ == "__main__":
    
    # File Name
    Name = 'TOMATO2'
    PROExt = '.PRO'
    dotPROName = Name + PROExt

    OUTExt = '.OUT'
    dotOUTName = Name + 'PROday' + OUTExt



    ## Initialization
    # Copy a .PRO backup with .PRO.BACKUP
    copyDotPROFile( dotPROName )

    # Store the end of simu-day to variable to control simulation loop
    configList = readDotPROFile( dotPROName )
    # print( configList )

    firstSimuDay = int(configList[1])
    lastSimuDay =  int(configList[2])
    firstCropDay =  int(configList[3])
    lastCropDay =  int(configList[4])
    
    # print( 'firstSimuDay:{}'.format( firstSimuDay ) )
    # print( 'lastSimuDay:{}'.format( lastSimuDay ) )
    # Set Initial simu-day and crop-day in .PRO with frist Day+1 day interval
    # IntervalFirstSimuDay = firstSimuDay
    # IntervalLastSimuDay = firstSimuDay + 1
    # replaceDotPRObyLine( dotPROName, 4, str( IntervalLastSimuDay ) )
    

    ## Do First Simulation to generate whole moisture(VWC) variation
    executeAquaCropPlugin()
    pathOUT = prefixOUT + dotOUTName
    dailyData = np.loadtxt( pathOUT, skiprows=4 )
    

    ## PROday.OUT index Memo
    rainIdx = 6
    irrIdx = 7
    WC1Idx = 62
    WC2Idx = 63

    currentSimuDay = firstSimuDay
    dailyDatPointer = 0
    while( currentSimuDay < lastSimuDay ):
        print ( 'CurrentSimuDay: {}\n'.format( currentSimuDay ) )
        print ( 'dailyDatPointer: {}\n'.format( dailyDatPointer ) )
    #    # if the currentSimuDay reach the lastSimuDay in config,  terminate the simulation
    #     if currentSimuDay == lastSimuDay:
    #         break

        dailyData = np.loadtxt( pathOUT, skiprows=4 )
        row = dailyData[ dailyDatPointer ]
        wc1 = row[ WC1Idx ]
        wc2 = row[ WC2Idx ]
        print( 'wc1: {}, wc2: {} \n'.format( wc1, wc2 ))

        # If moisture condition triggers irrigation event, controller to generate irrigation amount 
        predictedIrri = mockControllerBySI( wc1, wc2 )
        print( 'Irri: {}\n'.format( predictedIrri ))

        if predictedIrri > 0:
            # Append Irrigatio Event into Example.Irr
            irriDay = dailyDatPointer + 1
            appendDotIRR('Example.Irr', irriDay, predictedIrri )

            # Re-simulation the whole procces ()
            executeAquaCropPlugin()

        currentSimuDay = currentSimuDay + 1
        dailyDatPointer = dailyDatPointer + 1

