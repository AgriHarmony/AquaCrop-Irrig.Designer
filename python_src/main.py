
import subprocess
import os
import numpy as np
from pathlib import Path

prefix = '../bin/aquacrop_plug_in_v5_0/LIST/'
prefixOut = '../bin/aquacrop_plug_in_v5_0/OUTP/'

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

def writeDotPROFile( fileName, lineNum, contentStr ):
    # lineNum is start with index = 0

    sourceFilePath = Path(prefix+fileName).resolve()
    print ( sourceFilePath )
    f = open( sourceFilePath, 'r+' )
    
    lines = f.readlines()
    if lineNum < len(lines) :
        seg2 = lines[lineNum].split(':')[1] 
        lines[lineNum] = contentStr + ' : ' +  seg2
        # print ( lines[lineNum] )
    f.close()
    out = open( sourceFilePath, 'w' )
    out.writelines( lines )
    out.close()

if __name__ == "__main__":
    
    # File Name
    Name = 'TOMATO2'
    PROExt = '.PRO'
    dotPROName = Name + PROExt

    OUTExt = '.OUT'
    dotOUTName = Name + 'PROday' + OUTExt

    # Location
    pluginExeLocation = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\ACsaV50.exe'

    ## Initialization
    # Copy a .PRO backup with .PRO.BACKUP
    copyDotPROFile( dotPROName )

    # Store the end of simu-day to variable to control simulation loop
    configList = readDotPROFile( dotPROName )
    
    firstSimuDay = int(configList[2])
    lastSimuDay =  int(configList[3])
    firstCropDay =  int(configList[4])
    lastCropDay =  int(configList[5])
    
    # Set Initial simu-day and crop-day in .PRO with frist Day+1 day interval
    # IntervalFirstSimuDay = firstSimuDay
    # IntervalLastSimuDay = firstSimuDay + 1
    # writeDotPROFile( dotPROName, 4, str( IntervalLastSimuDay ) )
    

    ## Do First Simulation to generate whole moisture(VWC) variation
    subprocess.call([pluginExeLocation])    
    # Trace the input depth of moisture value 
        # If moisture condition triggers irrigation event, controller to generate irrigation amount 
    
    dayData = np.loadtxt( prefixOut + dotOUTName )
    print( dayData )
        # Write to Example.Irr file
        # if the currentSimuDay is not reach the lastSimuDay in config
            # Re-simulation the whole procces ()
        # otherwise, terminate the simulation



    ## loop Simulate with daily time step
    # while( IntervalLastSimuDay <= lastSimuDay ):

        # print ( str(IntervalLastSimuDay) + "\n")
        # Wrtie control preidction Irrgiation to file
    
        # Execute AquaCrop-Plugin
        
        # Move the simulation time windows to next day interval in .PRO
        # IntervalFirstSimuDay += 1
        # IntervalLastSimuDay += 1
    
