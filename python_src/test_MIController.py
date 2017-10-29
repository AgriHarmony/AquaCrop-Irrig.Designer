from Controller.Controller import Controller
from Controller.Controller import SimpleController
from Configuration import ConfigHolder
import numpy as np
import random
import unittest


def genRandomWaterContentSeqList(length, wcMin, wcMax):
    randomWCList = []
    for i in range(length):
        randomWCList.append(random.uniform(wcMin, wcMax))
    return randomWCList


def genSimuDaySeqList(length):
    return [i for i in range(length)]


def initializeSimpleControl():
    soilProperityDict = {"sat": 50, "fc": 30, "pwp": 10}
    soilProfile = {"compartment_num": 7}
    sensorIntepret = {"controlPoint": 1, "feedbackPoint": -1}

    simpleCtl = SimpleController(
        soilProperityDict, soilProfile, sensorIntepret)
    simpleCtl.set_ref(np.array([30, 30, 30, 30, 30, 30, 30]))
    simpleCtl.set_k(np.array([1.5, 0, 0, 0, 0, 0, 0]))
    return simpleCtl

# test SimpleController


class SimpleControllerTest(unittest.TestCase):

    def test_simpleController_vector(self):
        soilPropertyDict = {"sat": 50, "fc": 30, "pwp": 20}
        simpleCtler = SimpleController(soilPropertyDict)
        simpleCtler.set_ref(np.array([]))

    def test_writeout(self):
        simpleCtl = initializeSimpleControl()
        simpleCtl.writout


if __name__ == '__main__':

    unittest.main()
