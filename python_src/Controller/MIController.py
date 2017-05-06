import time
class MIController():

    def __init__( self, ref1 = 25, ref2 = 17 ):
        
        self.ref1 = ref1
        self.ref2 = ref2

        self.kp = 0
        self.ki = 0
        self.kd = 0

        self.pterm = 0
        self.iterm = 0
        self.dterm = 0

        self.e1 = 0
        self.e2 = 0

        self.last_time = 0
        self.delta_time = 1
        self.sample_time = 1

        self.output = 0

        self.stateRecord = []
        self.stateDefintion = ['shallow, wet, deeper, wet','shallow, dry, deeper, wet', \
                    'shallow, dry, deeper, dry', 'shallow, dry, deeper, wet']

    def setK( self, kp, ki, kd ):

        self.kp = kp
        self.ki = ki
        self.kd = kd

    def update( self, wc1, wc2, simuDay ):

        self.e1 = wc1 - self.ref1
        self.e2 = wc2 - self.ref2
        e1 = self.e1
        e2 = self.e2

        error = 0
        state = ''

        # Problem: Should I combine to e1 and e2 into single error ?

        ## shallow wet, deeper wet, over-irrigation state
        if e1 < 0 and e2 < 0:
            state = self.stateDefintion[0]
            error = e1

        ## shallow dry, deeper wet
        elif e1 > 0 and e2 < 0 :
            state = self.stateDefintion[1]
            error = e1
              
        ## shallow dry, deeper dry
        elif e1 > 0 and e2 > 0 :
            state = self.stateDefintion[2]
            error = e1

        ## shallow wet, deeper dry
        elif e1 < 0 and e2 > 0 :
            state = self.stateDefintion[3]
            error = e1
            
        record = { 'state': state, 'simuDay': simuDay }
        self.stateRecord.append( record )
        # self.updatePID( error )
    # def updatePID( self, error ):
    
    def getStateRecord( self ):
        return self.stateRecord

    def getError1( self ):
        return self.e1
    
    def getError2( self ):
        return self.e2

    # def getOutput():
