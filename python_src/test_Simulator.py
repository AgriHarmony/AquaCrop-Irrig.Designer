from Simulator.EnvSimulator import EnvSimulator
from Configuration import ConfigHolder
import helper as helper
import numpy as np
import random
import unittest
import os
from pathlib import Path

# Global Variable for testing
cfgHolder = ConfigHolder()
config = cfgHolder.get()

COMMON_VARIABLES = {
    'PROJECT': 'TOMATO2'
}


class SimulatorTest(unittest.TestCase):

    # Common initilization of simulator
    def intiSimulation(self):

        envSimu = EnvSimulator(COMMON_VARIABLES['PROJECT'])
        envSimu.initRun()
        return envSimu

    def test_initRun(self):
        envSimu = self.intiSimulation()
        envSimu.initRun()

    @unittest.skip("skip integration test_runOnce_generate_dayOutput")
    def test_runOnce_generate_dayOutput(self):

        name = COMMON_VARIABLES['PROJECT']

        # Remove exist output
        day = config['path_prefix']['AC_plugin_OUTP'] + name + "PROday.OUT"
        season = config['path_prefix']['AC_plugin_OUTP'] + \
            name + "PROseason.OUT"

        dayFile = Path(day)
        seasonFile = Path(season)
        if dayFile.exists():
            os.remove(day)
        if seasonFile.exists():
            os.remove(season)

        # Test Run
        envSimu = EnvSimulator(name)
        envSimu.runOnce()
        # os.path.abspath(day)

        dayFile = Path(day)
        self.assertTrue(dayFile.exists())

    @unittest.skip("skip integration test_runOnce_generate_seasonOutput")
    def test_runOnce_generate_seasonOutput(self):

        name = COMMON_VARIABLES['PROJECT']

        # Remove exist output
        day = config['path_prefix']['AC_plugin_OUTP'] + name + "PROday.OUT"
        season = config['path_prefix']['AC_plugin_OUTP'] + \
            name + "PROseason.OUT"

        dayFile = Path(day)
        if dayFile.exists():
            os.remove(day)
        seasonFile = Path(season)
        if seasonFile.exists():
            os.remove(season)

       # Test Run
        envSimu = EnvSimulator(name)
        envSimu.runOnce()
        # os.path.abspath(day)

        seasonFile = Path(season)
        self.assertTrue(seasonFile.exists())

    @unittest.skip("skip integration test")
    def test_integration(self):

        envSimu = self.intiSimulation()
        print("test_integration")

        while not envSimu.isFinish():
            print("\nDay Count: {}".format(envSimu.currentDayCount))
            envSimu.loadResult()
            print(envSimu.getCurrentDayWCs())
            WCs = envSimu.getCurrentDayWCs()
            print(WCs[0])

            predictedIrri = helper.mockControllerBySI(WCs[0], 25)

            if predictedIrri > 0:

                irriDay = envSimu.currentDayCount + 1
                print("IrriDay: {}".format(irriDay))
                print("Irri: {}".format(predictedIrri))
                helper.appendDotIRR('Example.Irr', irriDay, predictedIrri)
                envSimu.runOnce()

            envSimu.increateTimeStep()

    @unittest.skip("silent")
    def test_buildOUTPath(self):

        envSimu = self.intiSimulation()
        name = COMMON_VARIABLES['PROJECT']
        src = envSimu.buildOUTSorucePath('day', name)

        print(str(src))
        # print(correctPath)
        # self.assertEqual(envSimu.buildOUTPath( 'day', name, 'test'), correctPath)

    @unittest.skip("silent")
    def test_copyResult2output(self):
        envSimu = self.intiSimulation()
        envSimu.runOnce()
        name = COMMON_VARIABLES['PROJECT']
        envSimu.writeOutResult(name, 'depth1_ref30')


if __name__ == '__main__':
    unittest.main()
