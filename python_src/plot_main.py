import datetime 
import plot as pt
import helper as helper

def plot_main():
    name = str(datetime.datetime.now()).replace(':','_').replace('.','_')

    absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\OUTP\TOMATO2PROday.OUT'
    absDestPath = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(name)
    helper.writeDayData2AlignedCSV(absSorucePath,absDestPath)

    absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\OUTP\TOMATO2PROseason.OUT'
    absDestPath = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_season.csv'.format(name)
    helper.writeSeasonData2AlignedCSV(absSorucePath,absDestPath)

    # plot Water Content in Layer
    dataSource = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(name)
    figureDest = 'D:\yk_research\AquaCrop-Irrigation-Design\output\{}.png'.format(name)
    pt.plotWClayer(dataSource, figureDest)
# if __name__ == "__main__":
#     plot_main()
    
