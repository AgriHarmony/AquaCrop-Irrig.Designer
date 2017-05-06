from Controller.MIController import MIController
from settings import ConfigHolder 
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

# test MI Controller TestCase
class MIControllerTest( unittest.TestCase ):

    def test_update_recordState(self):
        cfgHolder = ConfigHolder()
        config = cfgHolder.get()
        mic= MIController()
        mic.setK( config['controller_coefficient']['kp'], config['controller_coefficient']['ki'], \
                    config['controller_coefficient']['kd'] )
        
        mic.update(18, 35, 1)
        r = mic.getStateRecord()
        self.assertEqual(r[0]['state'], 'shallow: dry, deeper: wet')
    
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