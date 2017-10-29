import numpy as np
import helper as helper
import datetime
import plot as myPloyLib
from Controller.Controller import SimpleController
from Controller.Controller import SimpleController
from Configuration import ConfigHolder
from Simulator.EnvSimulator import EnvSimulator
from Algorithm.AlgorithmLog import AlgorithmLog
import plot as myplot


def initilzieController(config, ref):

    sensor0 = 0
    initialRef = ref

    soilProperityDict = {"sat": 50, "fc": 30, "pwp": 10}
    soilProfile = {"compartment_num": config["compartment_num"]}
    sensorIntepret = {"controlDepth": sensor0}
    simpleCtl = SimpleController(
        soilProperityDict, soilProfile, sensorIntepret)

    # Initialize reference of all layer
    refsArray = np.zeros(soilProfile['compartment_num'])
    refsArray[sensor0] = initialRef
    simpleCtl.set_ref(refsArray)

    # intialize PID k in all layer, Set Kp,Ki,Kd cefficient
    kArray = np.zeros((3, soilProfile['compartment_num']))
    kArrayIndex = simpleCtl.get_kArray_index()
    ku = 4
    tu = 0.7
    for i in range(0, soilProfile['compartment_num']):
        kArray[kArrayIndex['p'], i] = 0.45 * ku
        kArray[kArrayIndex['i'], i] = 0
        kArray[kArrayIndex['i'], i] = tu / 2
        kArray[kArrayIndex['d'], i] = 0
        # kArray[kArrayIndex['d'],sensor0]=tu/8
        simpleCtl.set_k(kArray)

    # Set windup
    simpleCtl.set_windup(50)
    return simpleCtl


def run_simulation(dynamicRef, mp, simulationName):

    project = 'TOMATO2'
    envSimu = EnvSimulator(project)
    envSimu.initRun()

    cfgHolder = ConfigHolder()
    config = cfgHolder.get()

    #
    # Initialize Controller
    #
    simpleCtl = initilzieController(config, dynamicRef)
    refsArray = simpleCtl.get_ref()
    sensor0 = simpleCtl.get_controDepth()
    dynamicRef = refsArray[sensor0]
    #
    # initilize algorithm log
    #
    al = AlgorithmLog()

    #
    # simulation main loop the whole season
    #
    while not envSimu.isFinish():

        print("\nDay Count: {}".format(envSimu.currentDayCount))

        envSimu.loadResult()

        # print("WCs:")
        # print(envSimu.getCurrentDayWCs())
        WCs = envSimu.getCurrentDayWCs()

        ##
        #    Methodology Part:
        #    If moisture condition triggers irrigation event, controller to generate irrigation amount
        ###

        ##
        # Find floating EWC( Efficient Wetting Zone )
        ##
        halfRootDepth = envSimu.getCurrentRootDepth() * mp
        compartment_boundary_list = config['compartment_boundary_list']
        closestCompartment = helper.calEWZbyCompartment(
            compartment_boundary_list, halfRootDepth)
        sensor0 = int(closestCompartment * 10 - 1)

        # print("moving sensor0: {}".format(sensor0))
        simpleCtl.set_controlDepth(sensor0)

        ##
        # *self-adapt with sensor0 and sensor1
        ##
        sensor1 = 0
        #
        # update ref0
        #
        # if WCs[sensor1] > 20 and refsArray[sensor0] > 28:
        #     dynamicRef = dynamicRef - 1
        refsArray[sensor0] = dynamicRef
        simpleCtl.set_ref(refsArray)
        # Display adaptive dynamicRef of sensor0
        print("sensor0 Ref: {}".format(dynamicRef))

        # # notate current sensor0 and sensor1 in soil layer
        # print("WCs:")
        # strWCs = list(map(str, envSimu.getCurrentDayWCs()))
        # strWCs[sensor0] = "*" + strWCs[sensor0]
        # # strWCs[sensor1] = "$" + strWCs[sensor1]
        # print(strWCs)

        # print("Refs:")
        # strRefsArray = list(map(str, simpleCtl.get_ref()))
        # strRefsArray[sensor0] = "*" + strRefsArray[sensor0]
        # # strRefsArray[sensor1] = "$" + strRefsArray[sensor1]
        # print(strRefsArray)

        # print("Error:")
        # strErrors = list(map(str, simpleCtl.get_error(WCs)))
        # strErrors[sensor0] = "*" + strErrors[sensor0]
        # # strErrors[sensor1] = "$" + strErrors[sensor1]
        # print(strErrors)

        ##
        # -- ET-base Irrigation --
        ##
        # ET_k = 1.15
        # predictedIrri = helper.ETbasedIrrigation(ET, ET_k)

        ##
        # -- MI-controller --: shallow point = 0.05m, 0.15m, 0.25m(wc1, wc2, wc3)
        ##
        # print("error:")
        # print(simpleCtl.get_error(WCs))
        predictedIrri = simpleCtl.get_output(WCs)
        controllerStatus = simpleCtl.get_status(WCs)

        logIrri = 0
        if predictedIrri > 0:
            logIrri = predictedIrri
            # irri Day is  currentDatCount add one due to we use
            # today's condition to decide tomorrow's irrigation amount
            irriDay = envSimu.currentDayCount + 1
            # print("IrriDay: {}".format(irriDay))
            # print("To Irrigate: {}".format(predictedIrri))
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
            envSimu.runOnce()

        logDict = {"dayCount": envSimu.currentDayCount + 1,
                   "WCs": envSimu.getCurrentDayWCs(),
                   "refs": simpleCtl.get_ref(),
                   "error": simpleCtl.get_error(WCs),
                   "pidk": simpleCtl.get_k(),
                   "sensor0_depth": sensor0,
                   "sensor1_depth": sensor1,
                   "irri": logIrri,
                   "CC": envSimu.getCurrentDayData()[29],
                   "Biomass": envSimu.getCurrentDayData()[36]}

        al.log(logDict)
        envSimu.increateTimeStep()

    # End the while loop

    # write out the day and season .csv file
    fileName = simulationName
    envSimu.writeOutResult(project, fileName)

    # Write out algorithm log file to csv
    seasonDataPath = r"D:\yk_research\AquaCrop-Irrigation-Design\output\{}_season.csv".format(
        fileName)
    seasonData = helper.loadSeasonCSV(seasonDataPath)

    algInfo = {'sensor0': 'sensor0', 'sensor1': 'sensor1',
               'ref0': 'ref0', 'ref1': 'ref1'}
    summary = {"yield": seasonData['Yield']
               [-1], "water": seasonData['Irri'][-1]}
    al.writeLogToCSV(algInfo, summary, fileName)


if __name__ == "__main__":

    #     dynamicRef = 35
    #     mp = 0.9
    #     run_simulation(dynamicRef, mp, "default")

    moving_presentage = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    references = [35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25]

    # resultList = []
    for mp in moving_presentage:
        for ref in references:

            print("start ref:{}, moving presentage:{}".format(ref, mp))

            # acquire an unique id for simulation
            sharedInfoPath = r"D:\yk_research\AquaCrop-Irrigation-Design\output\moving_control_point\shared_info.json"
            sharedInfo = helper.readSharedInfo(sharedInfoPath)

            simulationName = "{}ref_{}mp_{}id".format(
                ref, str(mp).replace('.', ''), sharedInfo["current_unique_id"])
            run_simulation(ref, mp, simulationName)

            # result = helper.extractYieldandTotalIrri(simulationName)
            # result['ref'] = ref
            # result['mp'] = mp
            # resultList.append(result)

            print("finish ref:{}, moving presentage:{}".format(ref, mp))

            # maintain an unique id for each simulation
            helper.increaseIdSharedInfo(sharedInfoPath)

            # plot
            dayDataPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_day.csv'.format(
                simulationName)
            logDataPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\{}_log.csv'.format(
                simulationName)
            myplot.plot_WC_layers(dayDataPath, logDataPath)
            myplot.plot_irrigation(logDataPath)
