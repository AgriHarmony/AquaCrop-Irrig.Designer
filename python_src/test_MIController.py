from Controller.MIController import MIController
from Controller.MIController import SimpleController
from Configuration import ConfigHolder 
import numpy as np
import random
import unittest


def genRandomWaterContentSeqList( length, wcMin, wcMax ):
     randomWCList = []
     for i in range( length ):
        randomWCList.append( random.uniform( wcMin, wcMax ) ) 
     return randomWCList

def genSimuDaySeqList( length ):
    return [ i for i in range( length )]

def initializeSimpleControl():
    soilProperityDict = {"sat":50, "fc":30, "pwp":10}
    soilProfile = {"compartmentNum":7}
    sensorIntepret = {"controlPoint":1, "feedbackPoint":-1}
    
    simpleCtl = SimpleController(soilProperityDict, soilProfile, sensorIntepret)
    simpleCtl.set_ref(np.array([30,30,30,30,30,30,30]))
    simpleCtl.set_k(np.array([1.5,0,0,0,0,0,0]))
    return simpleCtl

# test SimpleController
class SimpleControllerTest( unittest.TestCase ):
    
    def test_simpleController_vector(self):
        soilPropertyDict = {"sat":50, "fc":30, "pwp":20}
        simpleCtler = SimpleController(soilPropertyDict)
        simpleCtler.set_ref(np.array([]))

    def test_writeout(self):
        simpleCtl = initializeSimpleControl()
        simpleCtl.writout

if __name__ == '__main__':

    # cfgHolder = ConfigHolder()
    # config = cfgHolder.get()
    # mic= MIController()
    # mic.setK( config['controller_coefficient']['kp'], config['controller_coefficient']['ki'], \
    #             config['controller_coefficient']['kd'] )
    
    # simuPeriod = 100 # Day
    # simuDays = genSimuDaySeqList( simuPeriod )
    # wc1s = genRandomWaterContentSeqList( simuPeriod, 0.17, 0.5 )
    # wc2s = genRandomWaterContentSeqList( simuPeriod, 0.17, 0.5 )


    # mic.update()
    unittest.main()