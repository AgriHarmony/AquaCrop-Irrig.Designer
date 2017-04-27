import numpy as np
import matplotlib.pyplot as plt

prefixOUT = '../bin/aquacrop_plug_in_v5_0/OUTP/'
HEADER_NUM = 4

def plotWaterContent( wcIndex = 62, ref = 25 ): 

    #  default draw most shallow water content value of simulation result
    Name = 'TOMATO2'
    OUTExt = '.OUT'
    dotOUTName = Name + 'PROday' + OUTExt
    pathOUT = prefixOUT + dotOUTName

    # load simulation result
    dailyData = np.loadtxt( pathOUT, skiprows=4 )
    dailyDataArray = np.array( dailyData )
    
    # Read row header of data
    header = []
    with open(pathOUT, 'r') as dotOut:        
        i = 0
        for line in dotOut:
            if i >= HEADER_NUM:
               break
            elif i == 3 or i == 2:
                header.append( [ item for item in line.split(' ')  if item != '' ] )
           
            i = i + 1
    
    ## Plot Data
    # wc1
    simuDayIdx = 3
    x = dailyDataArray[:, simuDayIdx]
    y = dailyDataArray[:, wcIndex]

    # ref1 
    x2 = x
    y2 = [ref] * len(x2)
    
    # plot diagram
    plt.plot( x, y, 'r-', x2, y2, 'g-')
    headerMetricIndex = wcIndex - 5
    plt.ylabel('water content,{} ( depth: {} m )'.format( header[0][wcIndex], header[1][headerMetricIndex] ))
    plt.xlabel('day')
    plt.show()


def plotError():
    print( 'hello plotError' )

def plotWeather():
    print( 'hello plotWeather' )

if __name__ == '__main__':
    plotWaterContent()