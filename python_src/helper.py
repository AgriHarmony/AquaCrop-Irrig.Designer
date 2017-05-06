from settings import ConfigHolder
from pathlib import Path
import subprocess
import os
import shutil

cfgHolder = ConfigHolder()
config = cfgHolder.get()
prefixLIST = config['path_prefix']['AC_plugin_LIST']
prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
prefixDATA = config['path_prefix']['AC_DATA']
prefixDotPROBACK = config['path_prefix']['dotPRO']

# Location
pluginExeLocation =  config['executable_path']

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
def cleanExampleDotIrrFile():
    fileName = 'Example.Irr'
    sourceFilePath = Path( prefixDATA + fileName +'.BACK' ).resolve()
    soruceFile = Path( sourceFilePath )
    print( sourceFilePath )

    # Generate target file path
    parentDirPath = os.path.dirname ( sourceFilePath )
    targetFilePath = parentDirPath + '/' + fileName 
    targetFile = Path( targetFilePath )
    print( targetFilePath )

    shutil.copy2( sourceFilePath, targetFilePath )
    # os.system( 'cp {} {}'.format(sourceFilePath, targetFilePath) )

def copyDotPROFile(fileName):
    # find source file path
    sourceFilePath = Path( prefixLIST+fileName ).resolve()
    soruceFile = Path( sourceFilePath )
    
    # Generate target file path
   
    targetFilePath =   prefixDotPROBACK + fileName + '.BACK'
    targetFile = Path( targetFilePath )

    # check file source is exist and file target is not exist 
    if soruceFile.is_file() and not targetFile.is_file():
        shutil.copy2( sourceFilePath, targetFilePath )
        # os.system( 'cp {} {}'.format(sourceFilePath, targetFilePath) )


def readDotPROFile(fileName):
    configList = []
    lineCnt = 0
    sourceFilePath = Path(prefixLIST+fileName).resolve()
    
    with open( sourceFilePath, 'r' ) as f:
        for line in f.readlines():
            
            if lineCnt >= 26:
                break
            if line is not "\n":
                el = line.split(':')[0].strip()
                if isfloat( el ):
                    configList.append( float( el ) )
                elif isint( el ):
                    configList.append( int( el ) )  
        
               
            lineCnt = lineCnt + 1
    f.close()
    return configList

def replaceDotPRObyLine(fileName, lineNum, contentStr):
    # lineNum is start with index = 0

    sourceFilePath = Path(prefixLIST+fileName).resolve()

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
    
    sourceFilePath = Path( prefixDATA + fileName ).resolve()
    with open( sourceFilePath, 'a') as f:
        irriEventStr = '\n{:6d} {:9.1f} {:12.1f}'.format( day, irriAmount, 0)
        f.write( irriEventStr )
def executeAquaCropPlugin():
     subprocess.call([pluginExeLocation])

def mockControllerBySI( wc1 ):

    kp = 1.5
    ki = 0
    kd = 0

    ref1 = 25
    ref2 = 17

    e1 = ref1 - wc1

    irri = e1*kp

    if irri < 0:
        irri = 0
    elif irri > 120:
        irri = 120

    return irri

     