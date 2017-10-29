import numpy as np
import helper as helper
import datetime
import plot_main as pm
from Controller.Controller import Controller
from Controller.Controller import SimpleController
from Configuration import ConfigHolder
from Simulator.EnvSimulator import EnvSimulator


def simulateOnce(t, d):

    simpleCtl = SimpleController()
    predictedIrri = 0
    while not envSimu.isFinish():

        print("\nDay Count: {}".format(envSimu.currentDayCount))
        envSimu.loadResult()

        print("WCs:")
        print(envSimu.getCurrentDayWCs())
        WCs = envSimu.getCurrentDayWCs()

        irrHistory = envSimu.getIrrigationHistory()
        # print(WCs[0])

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
        # predictedIrri = simpleCtl.get_output(WCs)

        # controllerStatus = simpleCtl.get_status(WCs)

        # IrriHistory

        if envSimu.currentDayCount == 0:
            yesterIrrStr = "No yesterday"
        else:
            yesterdayIdx = envSimu.currentDayCount - 1
            yesterIrrStr = str(irrHistory[yesterdayIdx])

        print("Yesterday Irri: {}".format(yesterIrrStr))

        # Reference (Target)
        # ref=" ".join(map(str,controllerStatus['ref']))
        # print("ref: ")
        # print(controllerStatus['ref'])

        # # Error of observation point
        # print("err:")
        # trancatedErrList = ['%.3f'%elem for elem in controllerStatus['e']]
        # print(trancatedErrList)

        # # Coefficient K
        # print("k:")
        # print(controllerStatus['k'])

        # # Initialization miControllerontroller
        # miController = Controller(ref1=25.0, ref2=10.0)
        # miController.setK(1.5, 2.25, 0, 0)

        # ##
        # # Find floating EWC( Efficient Wetting Zone )
        # ##
        # firstQuarter = rDepth * 0.5
        # compartment_boundary_list = config['compartment_boundary_list']
        # closestCompartment = helper.calEWZbyCompartment(
        #     compartment_boundary_list, firstQuarter)

        # EWZGrowIdx = int(closestCompartment * 10 - 1)
        # EWZBottomWaterContent = row[WC1Idx + EWZGrowIdx]
        if predictedIrri > 0:

            irriDay = envSimu.currentDayCount + 1
            print("IrriDay: {}".format(irriDay))
            print("Irri: {}".format(predictedIrri))
            helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
            envSimu.runOnce()

        envSimu.increateTimeStep()


if __name__ == "__main__":

    name = 'TOMATO2'
    envSimu = EnvSimulator(name)
    envSimu.initRun()

    T = [0.05]
    D = [20]

    for t in T:
        for d in D:
            simulateOnce(t, d)
