import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path
from Configuration import ConfigHolder
from Algorithm.AlgorithmLog import AlgorithmLog
from os import listdir
from os.path import isfile, join, basename

configHolder = ConfigHolder()
config = configHolder.get()

prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
HEADER_NUM = config['day_data_format']['HEADER_ROW_NUM']
prefixOutput = config['path_prefix']['output']


def plotWaterContent(depth, ref, simulationName, outputFigureName):

    targetWCIndex = config['day_data_index']['wc1'] + depth
    #  default draw most shallow water content value of simulation result
    fileType = 'day'
    path = str(Path(prefixOutput +
                    r'\ref_depth_matrix\data\{}_{}.csv'.format(simulationName, fileType)).resolve())

    # load simulation result
    # dailyData = np.loadtxt( path, skiprows=HEADER_NUM, delimiter="," )
    # dailyDataArray = np.array( dailyData )
    # print(dailyDataArray)
    colsDefString = "Day	Month	Year	DAP	Stage	WC(1.20)	Rain	Irri	Surf	Infilt	RO	Drain	CR	Zgwt	Ex	E	E/Ex	Trx	Tr	Tr/Trx	ETx	ET	ET/ETx	GD	Z	StExp	StSto	StSen	StSalt	CC	Kc(Tr)	Trx	Tr	Tr/Trx	WP	StBio	Biomass	HI	Yield	Brelative	WPet	WC(1.20)	Wr(1.00)	Z	Wr	Wr(SAT)	Wr(FC)	Wr(exp)	Wr(sto)	Wr(sen)	Wr(PWP)	SaltIn	SaltOut	SaltUp	Salt(1.20)	SaltZ	Z	ECe	ECsw	StSalt	Zgwt	ECgw	WC1	WC2	WC3	WC4	WC5	WC6	WC7	WC8	WC9	WC10	WC11	WC12	ECe1	ECe2	ECe3	ECe4	ECe5	ECe6	ECe7	ECe8	ECe9	ECe10	ECe11	ECe12	Rain	ETo	Tmin	Tavg	Tmax	CO2"
    colsDefTuple = tuple(colsDefString.split('\t'))
    dailyData = np.genfromtxt(
        path, delimiter=',', skip_header=HEADER_NUM, dtype=float, names=colsDefTuple)
    targetWC = colsDefTuple[targetWCIndex]
    # Plot Data
    # WC at depth

    x = dailyData['DAP']
    y = dailyData[targetWC]

    # ref
    x2 = x
    y2 = [ref] * len(x2)

    # plot diagram
    plt.plot(x, y, 'r-')
    plt.plot(x2, y2, 'g-')

    plt.ylabel('water content at  '.format(targetWC))
    plt.xlabel('day')
    # plt.show()
    pathFigureOut = str(
        Path(prefixOutput + r'{}_{}.png'.format(outputFigureName, fileType)).resolve())
    plt.savefig(pathFigureOut)
    plt.clf()


def plotAllWaterContent(depthList, ref, simulationName, outputFigureName):

    # synthesis data path
    fileType = 'day'
    # path = str(Path(prefixOutput +
    # r'\ref_depth_matrix\data\{}_{}.csv'.format(simulationName, fileType)
    # ).resolve())
    path = str(
        Path(prefixOutput + r'\{}_{}.csv'.format(simulationName, fileType)).resolve())
    # load all data
    colsDefString = "Day	Month	Year	DAP	Stage	WC(1.20)	Rain	Irri	Surf	Infilt	RO	Drain	CR	Zgwt	Ex	E	E/Ex	Trx	Tr	Tr/Trx	ETx	ET	ET/ETx	GD	Z	StExp	StSto	StSen	StSalt	CC	Kc(Tr)	Trx	Tr	Tr/Trx	WP	StBio	Biomass	HI	Yield	Brelative	WPet	WC(1.20)	Wr(1.00)	Z	Wr	Wr(SAT)	Wr(FC)	Wr(exp)	Wr(sto)	Wr(sen)	Wr(PWP)	SaltIn	SaltOut	SaltUp	Salt(1.20)	SaltZ	Z	ECe	ECsw	StSalt	Zgwt	ECgw	WC1	WC2	WC3	WC4	WC5	WC6	WC7	WC8	WC9	WC10	WC11	WC12	ECe1	ECe2	ECe3	ECe4	ECe5	ECe6	ECe7	ECe8	ECe9	ECe10	ECe11	ECe12	Rain	ETo	Tmin	Tavg	Tmax	CO2"
    colsDefTuple = tuple(colsDefString.split('\t'))
    dailyData = np.genfromtxt(
        path, delimiter=',', skip_header=HEADER_NUM, dtype=float, names=colsDefTuple)

    # Plot Data
    # WC at depth
    for d in depthList:
        targetWCIndex = config['day_data_index']['wc1'] + d
        targetWCName = colsDefTuple[targetWCIndex]
        x = dailyData['DAP']
        y = dailyData[targetWCName]
        plt.plot(x, y, linestyle='--', label=targetWCName)

    # ref
    x2 = x
    y2 = [ref] * len(x2)
    plt.plot(x2, y2, 'g-')
    # plot diagram

    plt.legend(loc=2)
    plt.ylabel('all water content')
    plt.xlabel('day')
    # plt.show()
    pathFigureOut = str(
        Path(prefixOutput + r'{}_{}.png'.format(outputFigureName, fileType)).resolve())
    plt.savefig(pathFigureOut)
    plt.clf()


def plotWClayer(dataSource, figureDest):

    dailyData = np.loadtxt(dataSource, delimiter=',', skiprows=HEADER_NUM)

    # subplot preparation
    fig, axs = plt.subplots(3, 1,  figsize=(6, 9))
    # fig.subplots_adjust(left=0.02, bottom=0.06, right=0.95, top=0.94,
    # wspace=0.05)

    ##
    # plot WC layer content
    ##
    wc1 = config['day_data_index']['wc1']
    wc8 = wc1 + 8
    WClayer = np.transpose(dailyData[:, wc1:wc8])
    axs[0].set_title('Water Content Layer')
    im1 = axs[0].imshow(WClayer, aspect='auto', cmap='RdYlBu')

    ##
    # plot water balacne (inflow: irriIdx, rainIdx and output: drainage, ETidx)
    ##

    # time for x
    dapIdx = config['day_data_index']['DAP']
    dapData = np.transpose(dailyData[:, dapIdx])
    # inflow
    irriIdx = config['day_data_index']['irrigation']
    rainIdx = config['day_data_index']['rain']
    # outflow
    ETidx = config['day_data_index']['ET']

    axs[1].set_title('Water Balacne Inflow/Outflow')
    # axs[1].set_xlabel('day')
    axs[1].set_ylabel('water unit(mm)')
    axs[1].set_xlim(1, len(dapData))

    irriData = np.transpose(dailyData[:, irriIdx])
    rainData = np.transpose(dailyData[:, rainIdx])
    ETData = -1 * np.transpose(dailyData[:, ETidx])

    axs[1].plot(dapData, irriData, '.b', label='irri')
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
    # efficient root zone condition
    ##

    axs[2].set_title('Effective Zoot Zone Wr')
    axs[2].set_xlabel('day')
    axs[2].set_ylabel('water unit(mm)')
    axs[2].set_xlim(1, len(dapData))

    WrEZZIdx = config['day_data_index']['WCtotal'] + 3
    WrEZZ_SAT_Idx = config['day_data_index']['WCtotal'] + 4
    WrEZZ_FC_Idx = config['day_data_index']['WCtotal'] + 5
    WrEZZ_PWP_Idx = config['day_data_index']['WCtotal'] + 9

    WrEZZ_Data = np.transpose(dailyData[:, WrEZZIdx])
    WrEZZ_SAT_Data = np.transpose(dailyData[:, WrEZZ_SAT_Idx])
    WrEZZ_FC_Data = np.transpose(dailyData[:, WrEZZ_FC_Idx])
    WrEZZ_PWP_Data = np.transpose(dailyData[:, WrEZZ_PWP_Idx])

    axs[2].plot(dapData, WrEZZ_Data, 'b.', label='Wr')
    axs[2].plot(dapData, WrEZZ_SAT_Data, 'g--', label='SAT_Wr')
    axs[2].plot(dapData, WrEZZ_FC_Data, 'y--', label='FC_Wr')
    axs[2].plot(dapData, WrEZZ_PWP_Data, 'r--', label='PWP_Wr')

    axs[2].legend(loc='upper left')
    # plt.show()
    plt.savefig(figureDest)


def plot_WC_layers(dayDataPath, logDataPath):

    # load day data
    colsDefTuple = configHolder.getCSVDayDataColumnTuple()
    dailyData = np.genfromtxt(
        dayDataPath, delimiter=',', skip_header=HEADER_NUM,
        dtype=float, names=colsDefTuple)

    WCs = dailyData[['WC1', 'WC2', 'WC3', 'WC4',
                     'WC5', 'WC6', 'WC7', 'WC8', 'WC9', 'WC10']]
    root = dailyData['Z']
    data = np.transpose([list(r) for r in WCs])

    fig, ax = plt.subplots()
    # plot water content in all vertical compartments
    cax = ax.imshow(data, interpolation='none', cmap="Spectral", extent=[
        0, len(root), -1, 0], aspect="auto")

    # plot depth of root
    reversedRoot = -1 * root
    ax.plot(reversedRoot)

    # load log data
    algLog = AlgorithmLog()
    logHeader = tuple(algLog.getHeader())
    logData = np.genfromtxt(
        logDataPath, delimiter=',', skip_header=3,
        dtype=float, names=logHeader)

    # plot sensor0 track
    revSensor0TrackList = -1 * \
        (np.array(logData['sensor0_depth']) * 10 + 5) * 0.01
    ax.plot(revSensor0TrackList, color="red")

    # plot sensor1 track
    # revSensor1TrackList = -1 * \
    #     (np.array(logData['sensor1_depth']) * 10 + 5) * 0.01
    # ax.plot(revSensor1TrackList, color="green")

    # color bar
    cbar = fig.colorbar(cax, orientation='horizontal')

    ax.set_xlabel('Time(day)')
    ax.set_ylabel('Soil Depth(m)')
    ax.set_title("sensor0 start at {}cm and ref={}")
    pathFigureOut = str(Path(
        prefixOutput + r'{}_All_WC_root.png'.format(
            basename(dayDataPath).split('.')[0])).resolve())
    plt.savefig(pathFigureOut)
    plt.clf()


def plot_irrigation(logDataPath):

    # load log data
    algLog = AlgorithmLog()
    logHeader = tuple(algLog.getHeader())
    logData = np.genfromtxt(
        logDataPath, delimiter=',', skip_header=3,
        dtype=float, names=logHeader)
    name = basename(logDataPath).split('.')[0]
    fig, ax = plt.subplots()
    ax.scatter(logData['dayCount'], logData['Irri'])
    ax.set_xlabel('Time(day)')
    ax.set_ylabel('Irrigation(mm)')
    ax.set_title('Irrigation of {}'.format(name))
    pathFigureOut = str(Path(
        prefixOutput + r'{}_irri.png'.format(name)).resolve())
    plt.savefig(pathFigureOut)
    plt.clf()
