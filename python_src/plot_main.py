import datetime 
import helper as helper
import plot as myplot
from os import listdir
from os.path import isfile, join

# deplicated
def plot_main():
    
    name = str(datetime.datetime.now()).replace(':','_').replace('.','_')
    # plot Water Content in Layer
    dataSource = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(name)
    figureDest = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}.png'.format(name)
    myplot.plotWClayer(dataSource, figureDest)
    # pt.plotSingleWC()

def plot_depth_ref_all_WC():
    
    # all simulation combination results( define as simulationName )
    # R = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
    # D = [0,1,2,3,4]
    
    # Interested Simulation Data
    R = [36,37,38,39,40]
    D = [0,1,2,3,4]

    # Interested WC variation in different depth of soil
    observedDepth = [0,1,2,3,4]
    for r in R:
        for d in D:
            simulationName = 'depth{}_ref{}'.format(d,r)
            outputFigureName = '{}_all'.format(simulationName)
            myplot.plotAllWaterContent( observedDepth, r, simulationName, outputFigureName)



if __name__ == "__main__":
    # plot_depth_ref_all_WC()
    myplot.plot_img_test()
