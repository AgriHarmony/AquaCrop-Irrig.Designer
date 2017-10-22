import numpy as np
import helper as helper
import datetime
import plot as myPloyLib
from Controller.MIController import MIController
from Controller.MIController import SimpleController
from settings import ConfigHolder
from Simulator.EnvSimulator import EnvSimulator


if __name__ == "__main__":

    project = 'TOMATO2'
    envSimu = EnvSimulator(project)
    envSimu.initRun()

    cfgHolder = ConfigHolder()
    config = cfgHolder.get()

    #
    # Initialize Controller
    #
    depth = 0
    ref = 20
    originalRef = ref
    predictedIrri = 0
    soilProperityDict = {"sat": 50, "fc": 30, "pwp": 10}
    soilProfile = {"compartmentNum": 10}
    sensorIntepret = {"controlDepth": depth}
    simpleCtl = SimpleController(
        soilProperityDict, soilProfile, sensorIntepret)

    # Initialize reference of all layer
    refsArray = np.zeros(soilProfile['compartmentNum'])
    refsArray[depth] = ref
    simpleCtl.set_ref(refsArray)

    # intialize PID k in all layer, Set Kp,Ki,Kd cefficient
    kArray = np.zeros((3, soilProfile['compartmentNum']))
    kArrayIndex = simpleCtl.get_kArray_index()
    ku = 4
    tu = 0.7
    for i in range(0, soilProfile['compartmentNum']):
        kArray[kArrayIndex['p'], i] = 0.45 * ku
        kArray[kArrayIndex['i'], i] = 0
        kArray[kArrayIndex['i'], i] = tu / 2
        kArray[kArrayIndex['d'], i] = 0
        # kArray[kArrayIndex['d'],depth]=tu/8
        simpleCtl.set_k(kArray)
    print("PID K")
    print(kArray)

    # Set windup
    simpleCtl.set_windup(50)

    #
    # end of intialize controller
    #

    # declare controller output
    statusList = []
    statusList.append("day,sensor0depth,sensor1depth\n")
    sensor0TrackList = []
    sensor1TrackList = []

    #
    # simulation main loop the whole season
    #
    while not envSimu.isFinish():

        print("\nDay Count: {}".format(envSimu.currentDayCount))
        envSimu.loadResult()

        # print("WCs:")
        # print(envSimu.getCurrentDayWCs())
        WCs = envSimu.getCurrentDayWCs()

        # irrHistory = envSimu.getIrrigationHistory()
        # print(WCs[0])

        """
            Methodology Part:
            If moisture condition triggers irrigation event, controller to generate irrigation amount
        """

        # # IrriHistory

        # if envSimu.currentDayCount == 0:
        #     yesterIrrStr = "No yesterday"
        # else:
        #     yesterdayIdx = envSimu.currentDayCount - 1
        #     yesterIrrStr = str(irrHistory[yesterdayIdx])

        ##
        # Find floating EWC( Efficient Wetting Zone )
        ##
        halfRootDepth = envSimu.getCurrentRootDepth() * 0.1
        compartmentBoundary = config['compartmentBoundary']
        closestCompartment = helper.calEWZbyCompartment(
            compartmentBoundary, halfRootDepth)
        sensor0 = int(closestCompartment * 10 - 1)

        print("moving sensor0: {}".format(sensor0))
        simpleCtl.set_controlDepth(sensor0)
        sensor0TrackList.append(sensor0)

        ##
        # *self-adapt with sensor0 and sensor1
        ##
        sensor1 = sensor0 + 3
        sensor1TrackList.append(sensor1)

        # update ref0
        # if WCs[sensor1] > 20 and refsArray[sensor0] > 28:
        #     ref = ref - 1
        refsArray[sensor0] = ref

        # # global static ref0
        # staticRef0 = [35, 32, 31, 30, 29]
        # staticRef0 = [35, 33, 32, 31, 30]
        # refsArray[sensor0] = staticRef0[sensor0]
        # ref = staticRef0[sensor0]
        # Display adaptive ref of sensor0
        print("sensor0 Ref: {}".format(ref))
        simpleCtl.set_ref(refsArray)

        # notate current sensor0 and sensor1 in soil layer
        print("WCs:")
        strWCs = list(map(str, envSimu.getCurrentDayWCs()))
        strWCs[sensor0] = "*" + strWCs[sensor0]
        # strWCs[sensor1] = "$" + strWCs[sensor1]
        print(strWCs)

        print("Refs:")
        strRefsArray = list(map(str, refsArray))
        strRefsArray[sensor0] = "*" + strRefsArray[sensor0]
        # strRefsArray[sensor1] = "$" + strRefsArray[sensor1]
        print(strRefsArray)

        print("Error:")
        strErrors = list(map(str, simpleCtl.get_error(WCs)))
        strErrors[sensor0] = "*" + strErrors[sensor0]
        # strErrors[sensor1] = "$" + strErrors[sensor1]
        print(strErrors)

        
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

        statusList.append("{},{},{}".format(envSimu.getCurrentDayCount(), sensor0, sensor1))
        if predictedIrri > 0:

            irriDay = envSimu.currentDayCount + 1
            print("IrriDay: {}".format(irriDay))
            print("To Irrigate: {}".format(predictedIrri))
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
            envSimu.runOnce()

        envSimu.increateTimeStep()

    # End the while loop

    # Write out the result
    sharedInfoPath = r"D:\yk_research\AquaCrop-Irrigation-Design\output\moving_control_point\shared_info.json"
    sharedInfo = helper.readSharedInfo(sharedInfoPath)

    simulationName = "depth{}_ref{}_moving_{}".format(
        depth, originalRef, sharedInfo["current_unique_id"])
    envSimu.writeOutResult(project, simulationName)
    helper.increaseIdSharedInfo(sharedInfoPath)

    # create single experiment notes
    # expJSONdestPath = "D:\yk_research\AquaCrop-Irrigation-Design\output\moving_control_point\{}.json".format(simulationName))
    # helper.createExpJSON(sharedInfoPath, expJSONdestPath)

    # Plot WC color diagram
    myPloyLib.plot_img_test(sensor0TrackList, sensor1TrackList)
