
import numpy as np
import helper as helper
from Controller.MIController import MIController
from settings import ConfigHolder


if __name__ == "__main__":
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

    ## Initialization
    # Copy a .PRO backup with .PRO.BACKUP
    helper.copyDotPROFile( dotPROName )

    # Store the end of simu-day to variable to control simulation loop
    configList = helper.readDotPROFile( dotPROName )
    # print( configList )

    firstSimuDay = int(configList[1])
    lastSimuDay =  int(configList[2])
    firstCropDay =  int(configList[3])
    lastCropDay =  int(configList[4])
    # print( 'firstSimuDay:{}'.format( firstSimuDay ) )
    # print( 'lastSimuDay:{}'.format( lastSimuDay ) )

    ## Do First Simulation to generate whole moisture(VWC) variation
    helper.cleanExampleDotIrrFile()
    helper.executeAquaCropPlugin()
    pathOUT = prefixOUTP + dotOUTName
    dailyData = np.loadtxt( pathOUT, skiprows=4 )

    
    ## PROday.OUT index Memo
    WC1Idx = config['day_data_index']['wc1']
    WC2Idx = config['day_data_index']['wc1'] + 1
    WC3Idx = config['day_data_index']['wc1'] + 2
    WC4Idx = config['day_data_index']['wc1'] + 3

    # Initialization MIController
    mic = MIController() 

    currentSimuDay = firstSimuDay
    dailyDataPointer = 0
    while( currentSimuDay < lastSimuDay ):

        # print ( 'CurrentSimuDay: {}\n'.format( currentSimuDay ) )
        # print ( 'dailyDataPointer: {}\n'.format( dailyDataPointer ) )

        dailyData = np.loadtxt( pathOUT, skiprows=4 )
        row = dailyData[ dailyDataPointer ]
        wc3 = row[ WC3Idx ]
        wc4 = row[ WC4Idx ]
        # print( 'wc1: {}, wc2: {} \n'.format( wc1, wc2 ))

        # Record State
        # mic.update( wc3, wc4, dailyDataPointer )


        # If moisture condition triggers irrigation event, controller to generate irrigation amount 
        predictedIrri=helper.mockControllerBySI( wc3 )
        tmpError = 25 - wc3
        tmpIrr = 1.5 * tmpError
        # print( 'error: {}, 1.5*error= {}\n'.format(tmpError, tmpIrr))
        # print('Irri: {}\n\n'.format(str(predictedIrri)))


        if predictedIrri > 0:
            # Append Irrigatio Event into Example.Irr
            irriDay = dailyDataPointer + 1
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri )

            # Re-simulation the whole procces ()
            helper.executeAquaCropPlugin()

        currentSimuDay = currentSimuDay + 1
        dailyDataPointer = dailyDataPointer + 1
    
    # # Write out StateRecord
    # stateRecord = mic.getStateRecord()
    # statePath = r'../output/state_{}.txt'.format(name)
    # with open(statePath, 'w') as outFile:
    #     for row in stateRecord:
    #         outFile.write( 'state: {}, simuDay: {}\n'.format( row['state'], row['simuDay'] ) ) 
