import numpy as np
import helper as helper
import datetime
import plot as myplot
from Controller.Controller import Controller
from Controller.Controller import SimpleController
from Configuration import ConfigHolder
from Simulator.EnvSimulator import EnvSimulator


def simulateOnce(ref, depth, simulationName):

    project = 'TOMATO2'
    envSimu = EnvSimulator(project)
    envSimu.initRun()

    #
    # controller intialization
    #
    soilProperityDict = {"sat": 50, "fc": 30, "pwp": 10}
    soilProfile = {"compartment_num": 7}
    sensorIntepret = {"controlDepth": depth}
    simpleCtl = SimpleController(
        soilProperityDict, soilProfile, sensorIntepret)

    # Set refs
    refsArray = np.zeros(soilProfile['compartment_num'])
    refsArray[depth] = ref
    simpleCtl.set_ref(refsArray)

    # Set Kp,Ki,Kd cefficient
    kArray = np.zeros((3, soilProfile['compartment_num']))
    kArrayIndex = simpleCtl.get_kArray_index()

    ku = 4
    tu = 0.7
    kArray[kArrayIndex['p'], depth] = 0.45 * ku
    kArray[kArrayIndex['i'], depth] = 0
    kArray[kArrayIndex['i'], depth] = tu / 2
    kArray[kArrayIndex['d'], depth] = 0
    # kArray[kArrayIndex['d'],depth]=tu/8
    simpleCtl.set_k(kArray)

    # Set windup
    simpleCtl.set_windup(50)

    predictedIrri = 0

    while not envSimu.isFinish():

        # print("\nDay Count: {}".format(envSimu.currentDayCount))
        envSimu.loadResult()

        irrHistory = envSimu.getIrrigationHistory()
        if envSimu.currentDayCount == 0:
            yesterIrrStr = "No yesterday"
        else:
            yesterdayIdx = envSimu.currentDayCount - 1
            yesterIrrStr = str(irrHistory[yesterdayIdx])

        # print("Yesterday Irri: {}".format(yesterIrrStr))

        #
        # LoadData from first execution
        #

        WCs = envSimu.getCurrentDayWCs()
        # print("WCs:")
        # print(WCs)
        WCsnpArray = np.array(WCs)
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
        err = simpleCtl.get_error(WCsnpArray)
        # print("error")
        # print(err)
        predictedIrri = simpleCtl.get_output(WCsnpArray)

        """
            Find floating EWC( Efficient Wetting Zone )
        """
        # firstQuarter = rDepth * 0.5
        # compartment_boundary_list = config['compartment_boundary_list']
        # closestCompartment = helper.calEWZbyCompartment(
        #     compartment_boundary_list, firstQuarter)

        # EWZGrowIdx = int(closestCompartment * 10 - 1)
        # EWZBottomWaterContent = row[WC1Idx + EWZGrowIdx]

        if predictedIrri > 0:

            irriDay = envSimu.currentDayCount + 1
            # print("IrriDay: {}".format(irriDay))
            # print("Irri: {}".format(predictedIrri))
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
            envSimu.runOnce()

        envSimu.increateTimeStep()

    # Extract Yield and Irrigation Amount from simulation

    # Write result to .csv
    envSimu.writeOutResult(project, simulationName)


if __name__ == "__main__":

    # R = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
    # D = [0,1,2,3,4]

    R = [36, 37, 38, 39, 40]
    D = [1, 2, 3, 4]
    resultList = []
    for r in R:
        for d in D:

            simulationName = 'depth{}_ref{}'.format(d, r)
            outputFigureName = simulationName
            simulateOnce(r, d, simulationName)
            # myplot.plotWaterContent( d, r, simulationName, outputFigureName )
            result = helper.extractYieldandTotalIrri(simulationName)
            result['ref'] = r
            result['depth'] = d

            # print(result)
            resultList.append(result)
            print("finish ref:{}, depth:{}".format(r, d))

    helper.writeResultList(resultList)
