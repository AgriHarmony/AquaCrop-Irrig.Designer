
import numpy as np
import helper as helper
import datetime 
import plot_main as pm
from Controller.MIController import MIController
from settings import ConfigHolder



if __name__ == "__main__":

    # Configuration
    cfgHolder = ConfigHolder()
    config = cfgHolder.get()
    prefixLIST = config['path_prefix']['AC_plugin_LIST']
    prefixOUTP = config['path_prefix']['AC_plugin_OUTP']
    prefixIRR = config['path_prefix']['AC_DATA']

    # File name
    name = 'TOMATO2'
    PROExt = '.PRO'
    dotPROName = name + PROExt

    OUTExt = '.OUT'
    dotOUTName = name + 'PROday' + OUTExt

    # Initialization
    # Copy a .PRO backup with .PRO.BACKUP
    helper.copyDotPROFile(dotPROName)

    # Store the end of simu-day to variable to control simulation loop
    configList = helper.readDotPROFile(dotPROName)
    # print( configList )

    firstSimuDay = int(configList[1])
    lastSimuDay = int(configList[2])
    firstCropDay = int(configList[3])
    lastCropDay = int(configList[4])
    # print( 'firstSimuDay:{}'.format( firstSimuDay ) )
    # print( 'lastSimuDay:{}'.format( lastSimuDay ) )

    # Do First Simulation to generate whole moisture(VWC) variation
    helper.cleanExampleDotIrrFile()
    helper.executeAquaCropPlugin()
    pathOUT = prefixOUTP + dotOUTName
    dailyData = np.loadtxt(pathOUT, skiprows=4)

    # PROday.OUT index from settings.py
    WC1Idx = config['day_data_index']['wc1']
    WC2Idx = config['day_data_index']['wc1'] + 1
    WC3Idx = config['day_data_index']['wc1'] + 2
    WC4Idx = config['day_data_index']['wc1'] + 3
    WC5Idx = config['day_data_index']['wc1'] + 4
    WC6Idx = config['day_data_index']['wc1'] + 5
    WC7Idx = config['day_data_index']['wc1'] + 6
    WC8Idx = config['day_data_index']['wc1'] + 7
    zIdx = config['day_data_index']['zoot']
    ETIdx = config['day_data_index']['ET']
    rainIdx = config['day_data_index']['rain']

    # Initialization miControllerontroller
    miController = MIController(ref1=25.0, ref2=10.0)
    miController.setK(1.5, 2.25, 0, 0)

    
    compartmentBoundary = config['compartmentBoundary']
    
    # Start Iterate simulation loop, simulation start from day1
    # Predict how to irrigation at day2...
    currentSimuDay = firstSimuDay
    dailyDataPointer = 0
    predictedIrri = 0
    while(currentSimuDay < lastSimuDay):

        ##
        # Prompt Info.
        ##
        dayCount=currentSimuDay-firstSimuDay+1
        print('==== Simu day: {} ==== \n'.format(dayCount))

        dailyData = np.loadtxt(pathOUT, skiprows=4)
        row = dailyData[dailyDataPointer]
        wc1 = row[WC1Idx]
        wc2 = row[WC2Idx]
        wc3 = row[WC3Idx]
        wc4 = row[WC4Idx]
        wc5 = row[WC5Idx]
        wc6 = row[WC6Idx]
        wc7 = row[WC7Idx]
        wc8 = row[WC8Idx]
        rain = row[rainIdx]
        rDepth = row[zIdx]
        ET = row[ETIdx]
        ##
        # Find floating EWC( Efficient Wetting Zone )
        ##
        firstQuarter = rDepth * 0.5
        closestCompartment = helper.calEWZbyCompartment(
            compartmentBoundary, firstQuarter)

        EWZGrowIdx = int(closestCompartment * 10 - 1)
        EWZBottomWaterContent = row[WC1Idx + EWZGrowIdx]
        

        """
            Methodology Part:
            If moisture condition triggers irrigation event, controller to generate irrigation amount
        """
        
        ##
        # -- ET-base Irrigation --
        ##
        # ET_k = 1.15
        # predictedIrri = helper.ETbasedIrrigation(ET, ET_k)

        ##
        # -- SI-controller --: shallow point = 0.05m, 0.15m, 0.25m(wc1, wc2, wc3)
        ##
        predictedIrri = helper.mockControllerBySI(wc2, 25)

        ## -- MI-controller without floating EWC --
        ## fixed shallow and deep

        ## -- MI-controller with floating EWC --
        ## shallow point = 0.05m, 0.15m, 0.25m(wc1, wc2, wc3)
        # miController.update(shallow_wc, EWZBottomWaterContent, rain, dailyDataPointer+1)
        # predictedIrri = miController.get_output()
        shallow_wc = wc1
        ## -- MI-controller with EWC and adaptive --


        # state = miController.get_state(dayCount)
        # print(' state: {}\n'.format(state))
        # Filter out negative irrigation amount
        if predictedIrri > 0:

            # Append Irrigatio Event into Example.Irr
            # tomorrow = today+1
            irriDay = dayCount + 1
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)

            # Prompt Info.
            print('wc_shallow: {}, EWZ_bottom: {}, zDepth: {}, closest compartment: {} \n'.format(
                shallow_wc, EWZBottomWaterContent, firstQuarter, closestCompartment))
            e1 = miController.get_error1()
            e2 = miController.get_error2()
            print("e1: {}, e2: {}\n".format(e1, e2))
            print("Tomorrow( {} ) Irri: {:.2f} \n\n".format(irriDay, predictedIrri))

            # Re-simulation the whole procces () to evaluate add new irrigation event
            helper.executeAquaCropPlugin()
        else:
            predictedIrri = 0


        currentSimuDay = currentSimuDay + 1
        dailyDataPointer = dailyDataPointer + 1

pm.plot_main()

