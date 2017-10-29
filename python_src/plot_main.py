import datetime
import helper as helper
import plot as myplot
from os import listdir
from os.path import isfile, join

# deplicated


def plot_main():

    name = str(datetime.datetime.now()).replace(':', '_').replace('.', '_')
    # plot Water Content in Layer
    dataSource = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(
        name)
    figureDest = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}.png'.format(
        name)
    myplot.plotWClayer(dataSource, figureDest)
    # pt.plotSingleWC()


def plot_depth_ref_all_WC():

    # all simulation combination results( define as simulationName )
    # R = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
    # D = [0,1,2,3,4]

    # Interested Simulation Data
    R = [36, 37, 38, 39, 40]
    D = [0, 1, 2, 3, 4]

    # Interested WC variation in different depth of soil
    observedDepth = [0, 1, 2, 3, 4]
    for r in R:
        for d in D:
            simulationName = 'depth{}_ref{}'.format(d, r)
            outputFigureName = '{}_all'.format(simulationName)
            myplot.plotAllWaterContent(
                observedDepth, r, simulationName, outputFigureName)


def plot_selected_WC_layers_sources():
    nameList = ["24ref_09mp_id399", "25ref_09mp_id400", "26ref_09mp_id401",
                "27ref_09mp_id402", "28ref_09mp_id403", "29ref_09mp_id404", "30ref_09mp_id405"]

    # hard coding path
    for name in nameList:
        dayDataPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(
            name)
        logDataPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_log.csv'.format(
            name)
        myplot.plot_WC_layers(dayDataPath, logDataPath)
        myplot.plot_irrigation(logDataPath)


if __name__ == "__main__":
    # plot_depth_ref_all_WC()
    plot_selected_WC_layers_sources()
