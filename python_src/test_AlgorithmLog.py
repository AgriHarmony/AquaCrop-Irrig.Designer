from Algorithm.AlgorithmLog import AlgorithmLog
from Simulator.EnvSimulator import EnvSimulator
from Configuration import ConfigHolder
import helper as helper
import numpy as np
import random
import unittest
import os
from pathlib import Path
from Controller.Controller import SimpleController

cfgHolder = ConfigHolder()
config = cfgHolder.get()

prefixOutput = config['path_prefix']['output']


class AlgorithmLogTest(unittest.TestCase):

    def intiSimulation(self):

        COMMON_VARIABLES = {
            'PROJECT': 'TOMATO2'
        }
        envSimu = EnvSimulator(COMMON_VARIABLES['PROJECT'])
        envSimu.initRun()
        return envSimu

    def initController(self):
        depth = 0
        ref = 20
        soilProperityDict = {"sat": 50, "fc": 30, "pwp": 10}
        soilProfile = {"compartment_num": config["compartment_num"]}
        sensorIntepret = {"controlDepth": depth}
        simpleCtl = SimpleController(
            soilProperityDict, soilProfile, sensorIntepret)

        # Initialize reference of all layer
        refsArray = np.zeros(soilProfile['compartment_num'])
        refsArray[depth] = ref
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
            # kArray[kArrayIndex['d'],depth]=tu/8
            simpleCtl.set_k(kArray)
        # print("PID K")
        # print(kArray)

        # Set windup
        simpleCtl.set_windup(50)
        return simpleCtl

    def test_AlgorithmLog(self):
        algLog = AlgorithmLog()
        # print(algLog.getHeader())

    def test_log(self):

        envSimu = self.intiSimulation()
        simpleCtl = self.initController()
        algLog = AlgorithmLog()
        while not envSimu.isFinish():
            print("\nDay Count: {}".format(envSimu.currentDayCount))
            if envSimu.currentDayCount == 2:
                break
            envSimu.loadResult()
            # print(envSimu.getCurrentDayWCs())
            WCs = envSimu.getCurrentDayWCs()
            # print(WCs[0])

            predictedIrri = helper.mockControllerBySI(WCs[0], 25)

            if predictedIrri > 0:

                irriDay = envSimu.currentDayCount + 1
                # print("IrriDay: {}".format(irriDay))
                # print("Irri: {}".format(predictedIrri))
                helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
                envSimu.runOnce()

            sensor0 = 0
            sensor1 = 1
            logDict = {"dayCount": envSimu.currentDayCount,
                       "WCs": envSimu.getCurrentDayWCs(),
                       "refs": simpleCtl.get_ref(),
                       "error": simpleCtl.get_error(WCs),
                       "pidk": simpleCtl.get_k(),
                       "sensor0_depth": sensor0,
                       "sensor1_depth": sensor1,
                       "irri": predictedIrri,
                       "CC": envSimu.getCurrentDayData()[29],
                       "Biomass": envSimu.getCurrentDayData()[36]}
            algLog.log(logDict)

            envSimu.increateTimeStep()

            self.assertEqual(
                len(algLog.logLines[0].split(",")), len(algLog.getHeader()))

    def test_writeLogToCSV(self):

        envSimu = self.intiSimulation()
        simpleCtl = self.initController()
        algLog = AlgorithmLog()
        while not envSimu.isFinish():
            print("\nDay Count: {}".format(envSimu.currentDayCount))

            envSimu.loadResult()
            # print(envSimu.getCurrentDayWCs())
            WCs = envSimu.getCurrentDayWCs()
            # print(WCs[0])

            predictedIrri = helper.mockControllerBySI(WCs[0], 25)

            if predictedIrri > 0:

                irriDay = envSimu.currentDayCount + 1
                # print("IrriDay: {}".format(irriDay))
                # print("Irri: {}".format(predictedIrri))
                helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
                envSimu.runOnce()

            sensor0 = 0
            sensor1 = 1
            logDict = {"dayCount": envSimu.currentDayCount,
                       "WCs": envSimu.getCurrentDayWCs(),
                       "refs": simpleCtl.get_ref(),
                       "error": simpleCtl.get_error(WCs),
                       "pidk": simpleCtl.get_k(),
                       "sensor0_depth": sensor0,
                       "sensor1_depth": sensor1,
                       "irri": predictedIrri,
                       "CC": envSimu.getCurrentDayData()[29],
                       "Biomass": envSimu.getCurrentDayData()[36]}

            algLog.log(logDict)
            envSimu.increateTimeStep()

        simulationName = "test_simulation"
        algInfo = {'sensor0': 'sensor0', 'sensor1': 'sensor1',
                   'ref0': 'ref0', 'ref1': 'ref1'}
        summary = {"yield": 0, "water": 0}
        algLog.writeLogToCSV(algInfo, summary, simulationName)


if __name__ == '__main__':
    unittest.main()
