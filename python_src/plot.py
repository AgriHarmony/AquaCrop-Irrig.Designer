import numpy as np
import matplotlib.pyplot as plt
from settings import ConfigHolder
cfgHolder = ConfigHolder()
config = cfgHolder.get()

prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
HEADER_NUM = config['day_data_format']['HEADER_ROW_NUM']

def plotWaterContent( wcIndex = 62, ref = 25 ): 

    #  default draw most shallow water content value of simulation result
    Name = 'TOMATO2'
    OUTExt = '.OUT'
    dotOUTName = Name + 'PROday' + OUTExt
    pathOUT = prefixOUTP + dotOUTName

    # load simulation result
    dailyData = np.loadtxt( pathOUT, skiprows=HEADER_NUM )
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

def plotWClayer(dataSource):

    

    dailyData = np.loadtxt(dataSource, delimiter=',', skiprows=HEADER_NUM)
    
    # subplot preparation
    fig, axs = plt.subplots(3, 1,  figsize=(6, 9))
    # fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94, wspace=0.05)
    
    ##
    # plot WC layer content
    ##
    wc1 = config['day_data_index']['wc1']
    wc8 = wc1 + 8
    WClayer = np.transpose(dailyData[:,wc1:wc8])
    axs[0].set_title('Water Content Layer')
    im1 = axs[0].imshow(WClayer, aspect='auto', cmap='RdYlBu')

    
    ## 
    # plot water balacne (inflow: irriIdx, rainIdx and output: drainage, ETidx)
    ##

    # time for x
    dapIdx = config['day_data_index']['DAP']
    dapData = np.transpose(dailyData[:,dapIdx])
    # inflow
    irriIdx = config['day_data_index']['irrigation']
    rainIdx = config['day_data_index']['rain']
    # outflow
    ETidx = config['day_data_index']['ET']

    axs[1].set_title('Water Balacne Inflow/Outflow')
    # axs[1].set_xlabel('day')
    axs[1].set_ylabel('water unit(mm)')
    axs[1].set_xlim(1,len(dapData))

    irriData = np.transpose(dailyData[:,irriIdx])
    rainData = np.transpose(dailyData[:,rainIdx])
    ETData = -1*np.transpose(dailyData[:,ETidx])

    axs[1].plot(dapData, irriData,'.b', label='irri')
    axs[1].plot(dapData, rainData, '.c', label='rain')
    axs[1].plot(dapData, ETData, '.r', label='ET')
    axs[1].legend(loc='upper left')
    ## 
    # ColorBar
    ##
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im1, cax=cbar_ax)
    
    ##
    # efficient zoot zone condition
    ## 

    axs[2].set_title('Effective Zoot Zone Wr')
    axs[2].set_xlabel('day')
    axs[2].set_ylabel('water unit(mm)')
    axs[2].set_xlim(1,len(dapData))

    WrEZZIdx = config['day_data_index']['WCtotal']+3
    WrEZZ_SAT_Idx = config['day_data_index']['WCtotal']+4
    WrEZZ_FC_Idx = config['day_data_index']['WCtotal']+5
    WrEZZ_PWP_Idx = config['day_data_index']['WCtotal']+9

    WrEZZ_Data = np.transpose(dailyData[:,WrEZZIdx])
    WrEZZ_SAT_Data = np.transpose(dailyData[:,WrEZZ_SAT_Idx])
    WrEZZ_FC_Data = np.transpose(dailyData[:,WrEZZ_FC_Idx])
    WrEZZ_PWP_Data = np.transpose(dailyData[:,WrEZZ_PWP_Idx])
    
    print(WrEZZ_Data)

    axs[2].plot(dapData, WrEZZ_Data, 'b.', label='Wr')
    axs[2].plot(dapData, WrEZZ_SAT_Data,'g--', label='SAT_Wr')
    axs[2].plot(dapData, WrEZZ_FC_Data,'y--', label='FC_Wr')
    axs[2].plot(dapData, WrEZZ_PWP_Data,'r--', label='PWP_Wr')
    
    axs[2].legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    plotWaterContent(62, 25)
    plotWaterContent(63, 17)