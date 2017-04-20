import numpy as np
import matplotlib.pyplot as plt

prefixOUT = '../bin/aquacrop_plug_in_v5_0/OUTP/'

if __name__ == '__main__':
    Name = 'TOMATO2'
    OUTExt = '.OUT'
    dotOUTName = Name + 'PROday' + OUTExt
    
    pathOUT = prefixOUT + dotOUTName
    dailyData = np.loadtxt( pathOUT, skiprows=4 )
    dailyDataArray = np.array( dailyData )

    # wc1
    simuDayIdx = 3
    x = dailyDataArray[:, simuDayIdx]
   
    WC1Idx = 62
    y = dailyDataArray[:, WC1Idx]

    # ref1 
    x2 = x

    ref1 = 25
    y2 = [ref1] * len(x2)
    
    # plot diagram
    plt.plot( x, y, 'r-', x2, y2, 'g-')
    plt.ylabel('water content1( 0.05m )')
    plt.xlabel('day')
    plt.show()